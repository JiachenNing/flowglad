from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import re
import json
from datetime import datetime
from google import genai

from database import SessionLocal, Hotel, Flight, Attraction, init_db
from models import (
    TravelPlanRequest, ChatMessage, RecommendationsResponse,
    HotelResponse, FlightResponse, AttractionResponse,
    BookingRequest, BookingResponse
)

# Initialize Google AI client
client = genai.Client(api_key="AIzaSyB2IWaDW1A8W-WfNMOdFvNr2JhpbO5Fik4")

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Travel Agent API"}

def extract_locations(text: str) -> List[str]:
    """Extract location names from travel plan text"""
    locations = []
    # Common cities and countries
    common_locations = [
        "Tokyo", "Kyoto", "Hakone", "Japan",
        "Paris", "France", "Rome", "Italy", "Barcelona", "Spain",
        "London", "UK", "Berlin", "Germany", "Amsterdam", "Netherlands",
        "Europe", "Asia", "America", "USA"
    ]
    
    text_lower = text.lower()
    for loc in common_locations:
        if loc.lower() in text_lower:
            locations.append(loc)
    
    return locations

def extract_days(text: str) -> int:
    """Extract number of days from travel plan"""
    # Look for patterns like "7-day", "7 days", "seven days"
    patterns = [
        r'(\d+)[-\s]day',
        r'(\d+)\s+days?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return 1  # Default to 1 day

def parse_travel_plan(plan: str) -> dict:
    """Parse travel plan to extract information"""
    locations = extract_locations(plan)
    days = extract_days(plan)
    
    # Determine if plan is specific or general
    is_specific = len(locations) > 0 and days > 1
    
    return {
        "locations": locations,
        "days": days,
        "is_specific": is_specific,
        "original_plan": plan
    }

def filter_by_preferences(query_result, preferences: str) -> List:
    """Filter results based on user preferences"""
    if not preferences:
        return query_result
    
    preferences_lower = preferences.lower()
    filtered = []
    
    for item in query_result:
        # For hotels
        if hasattr(item, 'amenities'):
            if 'nature' in preferences_lower and 'mountain' in item.amenities.lower():
                filtered.append(item)
            elif 'chill' in preferences_lower and 'spa' in item.amenities.lower():
                filtered.append(item)
            elif 'family' in preferences_lower or 'parents' in preferences_lower:
                filtered.append(item)
            else:
                filtered.append(item)
        
        # For attractions
        elif hasattr(item, 'category'):
            if 'nature' in preferences_lower and item.category == 'nature':
                filtered.append(item)
            elif 'history' in preferences_lower and item.category == 'history':
                filtered.append(item)
            elif 'chill' in preferences_lower and item.category == 'nature':
                filtered.append(item)
            else:
                filtered.append(item)
        
        # For flights
        else:
            filtered.append(item)
    
    return filtered if filtered else query_result

@app.post("/api/travel-plan", response_model=RecommendationsResponse)
def process_travel_plan(request: TravelPlanRequest, db: Session = Depends(get_db)):
    """Process travel plan and return recommendations"""
    parsed = parse_travel_plan(request.plan)
    locations = parsed["locations"]
    days = parsed["days"]
    
    # If no specific locations, return popular choices
    if not locations or "europe" in request.plan.lower():
        hotels = db.query(Hotel).filter(Hotel.country.in_(["France", "Italy", "Spain"])).limit(6).all()
        flights = db.query(Flight).filter(Flight.destination.in_(["Paris", "Rome", "Barcelona"])).limit(5).all()
        attractions = db.query(Attraction).filter(Attraction.country.in_(["France", "Italy", "Spain"])).limit(6).all()
    else:
        # Filter by specific locations
        hotels = db.query(Hotel).filter(
            Hotel.city.in_(locations) | Hotel.country.in_(locations)
        ).limit(6).all()
        
        flights = db.query(Flight).filter(
            Flight.destination.in_(locations) | Flight.origin.in_(locations)
        ).limit(5).all()
        
        attractions = db.query(Attraction).filter(
            Attraction.city.in_(locations) | Attraction.country.in_(locations)
        ).limit(6).all()
    
    # Apply preferences if provided
    if request.preferences:
        hotels = filter_by_preferences(hotels, request.preferences)
        attractions = filter_by_preferences(attractions, request.preferences)
    
    return RecommendationsResponse(
        hotels=[HotelResponse(**{k: getattr(h, k) for k in HotelResponse.__fields__.keys()}) for h in hotels],
        flights=[FlightResponse(**{k: getattr(f, k) for k in FlightResponse.__fields__.keys()}) for f in flights],
        attractions=[AttractionResponse(**{k: getattr(a, k) for k in AttractionResponse.__fields__.keys()}) for a in attractions],
        days=days,
        current_day=1
    )

def get_ai_filtering_guidance(user_message: str, available_items: List, item_type: str) -> str:
    """Use Google AI to analyze user preferences and get filtering guidance"""
    try:
        # Create a description of available items for context
        items_summary = []
        for item in available_items[:10]:  # Limit to first 10 for context
            if item_type == "hotel":
                items_summary.append(f"- {item.name} in {item.city}: {item.description}, Amenities: {item.amenities}")
            elif item_type == "attraction":
                items_summary.append(f"- {item.name} in {item.city}: {item.description}, Category: {item.category}")
        
        prompt = f"""You are a travel recommendation assistant. The user has sent this preference: "{user_message}"

Available {item_type}s:
{chr(10).join(items_summary)}

Based on the user's preference, analyze what they want and respond with a JSON object containing:
- "keywords": array of important keywords to match (e.g., ["nature", "chill", "family-friendly"])
- "priority": what matters most (e.g., "nature over history", "budget-friendly", "luxury")
- "filter_logic": brief description of how to filter items

Respond ONLY with valid JSON, no other text."""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text
    except Exception as e:
        print(f"Error calling Google AI: {e}")
        return '{"keywords": [], "priority": "", "filter_logic": ""}'

@app.post("/api/chat", response_model=RecommendationsResponse)
def chat_with_agent(message: ChatMessage, db: Session = Depends(get_db)):
    """Handle chatbot messages and update recommendations using Google AI"""
    user_preferences = message.message
    
    # Parse original plan if provided
    if message.current_plan:
        parsed = parse_travel_plan(message.current_plan)
        locations = parsed["locations"]
        days = parsed["days"]
    else:
        locations = []
        days = 1
    
    # Get base recommendations
    if not locations:
        hotels = db.query(Hotel).limit(20).all()  # Get more to filter from
        flights = db.query(Flight).limit(10).all()
        attractions = db.query(Attraction).limit(20).all()
    else:
        hotels = db.query(Hotel).limit(20).all()
        
        flights = db.query(Flight).filter(
            Flight.destination.in_(locations) | Flight.origin.in_(locations)
        ).limit(10).all()
        
        attractions = db.query(Attraction).filter(
            Attraction.city.in_(locations) | Attraction.country.in_(locations)
        ).limit(20).all()
    
    # Use Google AI to get filtering guidance
    try:
        # Get AI guidance for hotels
        hotel_guidance = get_ai_filtering_guidance(user_preferences, hotels, "hotel")
        hotel_guidance_json = json.loads(hotel_guidance.strip().replace('```json', '').replace('```', ''))
        hotel_keywords = [k.lower() for k in hotel_guidance_json.get("keywords", [])]
        
        # Get AI guidance for attractions
        attraction_guidance = get_ai_filtering_guidance(user_preferences, attractions, "attraction")
        attraction_guidance_json = json.loads(attraction_guidance.strip().replace('```json', '').replace('```', ''))
        attraction_keywords = [k.lower() for k in attraction_guidance_json.get("keywords", [])]
        
        # Filter hotels based on AI guidance
        filtered_hotels = []
        debug_dict = {}
        for hotel in hotels:
            hotel_text = f"{hotel.name} {hotel.description} {hotel.amenities} {hotel.city} {hotel.country}".lower()
            score = sum(1 for keyword in hotel_keywords if keyword in hotel_text)
            debug_dict[hotel.name] = score
            print('!!!!!!!', hotel.name, score);
            if hotel_keywords:
                if score > 0 or any(kw in user_preferences.lower() for kw in hotel_keywords):
                    filtered_hotels.append((hotel, score))
            else:
                filtered_hotels.append((hotel, 0))
        
        # Sort by relevance score and take top 6
        filtered_hotels.sort(key=lambda x: x[1], reverse=True)
        hotels = [h[0] for h in filtered_hotels[:6]]
        
        # Filter attractions based on AI guidance
        filtered_attractions = []
        for attraction in attractions:
            attraction_text = f"{attraction.name} {attraction.description} {attraction.category}".lower()
            score = sum(1 for keyword in attraction_keywords if keyword in attraction_text)
            if attraction_keywords:
                if score > 0 or any(kw in user_preferences.lower() for kw in attraction_keywords):
                    filtered_attractions.append((attraction, score))
            else:
                filtered_attractions.append((attraction, 0))
        
        # Sort by relevance score and take top 6
        filtered_attractions.sort(key=lambda x: x[1], reverse=True)
        attractions = [a[0] for a in filtered_attractions[:6]]
        
    except Exception as e:
        print(f"Error processing AI guidance: {e}")
        # Fallback to simple filtering
        hotels = filter_by_preferences(hotels[:6], user_preferences.lower())
        attractions = filter_by_preferences(attractions[:6], user_preferences.lower())
    
    return RecommendationsResponse(
        hotels=[HotelResponse(**{k: getattr(h, k) for k in HotelResponse.__fields__.keys()}) for h in hotels],
        flights=[FlightResponse(**{k: getattr(f, k) for k in FlightResponse.__fields__.keys()}) for f in flights[:5]],
        attractions=[AttractionResponse(**{k: getattr(a, k) for k in AttractionResponse.__fields__.keys()}) for a in attractions],
        days=days,
        current_day=1
    )

@app.get("/api/recommendations/day/{day}", response_model=RecommendationsResponse)
def get_recommendations_for_day(day: int, locations: Optional[str] = None, db: Session = Depends(get_db)):
    """Get recommendations for a specific day"""
    loc_list = locations.split(",") if locations else []
    
    if not loc_list:
        hotels = db.query(Hotel).limit(6).all()
        flights = db.query(Flight).limit(5).all()
        attractions = db.query(Attraction).limit(6).all()
    else:
        hotels = db.query(Hotel).filter(
            Hotel.city.in_(loc_list) | Hotel.country.in_(loc_list)
        ).limit(6).all()
        
        flights = db.query(Flight).filter(
            Flight.destination.in_(loc_list) | Flight.origin.in_(loc_list)
        ).limit(5).all()
        
        attractions = db.query(Attraction).filter(
            Attraction.city.in_(loc_list) | Attraction.country.in_(loc_list)
        ).limit(6).all()
    
    return RecommendationsResponse(
        hotels=[HotelResponse(**{k: getattr(h, k) for k in HotelResponse.__fields__.keys()}) for h in hotels],
        flights=[FlightResponse(**{k: getattr(f, k) for k in FlightResponse.__fields__.keys()}) for f in flights],
        attractions=[AttractionResponse(**{k: getattr(a, k) for k in AttractionResponse.__fields__.keys()}) for a in attractions],
        days=7,  # Assume max days
        current_day=day
    )

@app.post("/api/book", response_model=BookingResponse)
def book_item(request: BookingRequest, db: Session = Depends(get_db)):
    """Handle booking requests"""
    booking_id = f"{request.type}_{request.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    if request.type == "hotel":
        hotel = db.query(Hotel).filter(Hotel.id == request.id).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return BookingResponse(success=True, message=f"Hotel {hotel.name} booked successfully!", booking_id=booking_id)
    
    elif request.type == "flight":
        flight = db.query(Flight).filter(Flight.id == request.id).first()
        if not flight:
            raise HTTPException(status_code=404, detail="Flight not found")
        return BookingResponse(success=True, message=f"Flight {flight.airline} from {flight.origin} to {flight.destination} booked successfully!", booking_id=booking_id)
    
    elif request.type == "attraction":
        attraction = db.query(Attraction).filter(Attraction.id == request.id).first()
        if not attraction:
            raise HTTPException(status_code=404, detail="Attraction not found")
        return BookingResponse(success=True, message=f"Ticket for {attraction.name} purchased successfully!", booking_id=booking_id)
    
    else:
        raise HTTPException(status_code=400, detail="Invalid booking type")

