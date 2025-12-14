from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import re
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np

from database import SessionLocal, Hotel, Flight, Attraction, init_db
from models import (
    TravelPlanRequest, ChatMessage, RecommendationsResponse,
    HotelResponse, FlightResponse, AttractionResponse,
    BookingRequest, BookingResponse
)
# Initialize sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

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
    # Common cities and countries - ordered by specificity (cities before countries)
    common_locations = [
        # Cities (more specific)
        "Tokyo", "Kyoto", "Hakone", "Paris", "Rome", "Barcelona", "London", 
        "Berlin", "Amsterdam", "Vienna", "Prague", "Dubai", "Singapore", 
        "Bangkok", "Sydney", "New York", "Los Angeles", "Istanbul", "Cairo", 
        "Rio de Janeiro", "Buenos Aires",
        # Countries (less specific)
        "Japan", "France", "Italy", "Spain", "UK", "Germany", "Netherlands",
        "Austria", "Czech Republic", "UAE", "Thailand", "Australia", "USA",
        "Turkey", "Egypt", "Brazil", "Argentina",
        # Regions
        "Europe", "Asia", "America"
    ]
    
    text_lower = text.lower()
    found_locations = []
    
    # Check for locations in order (cities first, then countries)
    for loc in common_locations:
        if loc.lower() in text_lower:
            found_locations.append(loc)
    
    # Remove duplicates while preserving order
    seen = set()
    for loc in found_locations:
        if loc not in seen:
            locations.append(loc)
            seen.add(loc)
    
    return locations

def extract_days(text: str) -> int:
    """Extract number of days from travel plan"""
    # Look for patterns like "7-day", "7 days", "7day", "seven days"
    patterns = [
        r'(\d+)[-\s]day',
        r'(\d+)day',
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

    # Extract locations from preferences as well (users may mention multiple locations)
    preference_locations = []
    if request.preferences:
        preference_locations = extract_locations(request.preferences)
    
    # Combine all locations from plan and preferences, remove duplicates
    all_locations = list(set(locations + preference_locations))
    
    # Filter by all locations
    if all_locations:
        hotels = db.query(Hotel).filter(
            Hotel.city.in_(all_locations[-1:]) | Hotel.country.in_(all_locations)
        ).all()
        
        flights = db.query(Flight).filter(
            Flight.destination.in_(all_locations[-1:]) | Flight.origin.in_(all_locations)
        ).all()
        
        attractions = db.query(Attraction).filter(
            Attraction.city.in_(all_locations[-1:]) | Attraction.country.in_(all_locations)
        ).all()
    else:
        # If no locations specified, get all items
        hotels = db.query(Hotel).all()
        flights = db.query(Flight).all()
        attractions = db.query(Attraction).all()
    
    # Apply preferences if provided
    # if request.preferences:
    #     hotels = filter_by_preferences(hotels, request.preferences)
    #     attractions = filter_by_preferences(attractions, request.preferences)
    
    return RecommendationsResponse(
        hotels=[HotelResponse(**{k: getattr(h, k) for k in HotelResponse.__fields__.keys()}) for h in hotels],
        flights=[FlightResponse(**{k: getattr(f, k) for k in FlightResponse.__fields__.keys()}) for f in flights],
        attractions=[AttractionResponse(**{k: getattr(a, k) for k in AttractionResponse.__fields__.keys()}) for a in attractions],
        days=days,
        current_day=1
    )

def calculate_similarity_scores(user_message: str, items: List, item_type: str) -> List[tuple]:
    """Calculate cosine similarity between user message and items using sentence transformers"""
    try:
        # Get user message embedding
        user_embedding = model.encode([user_message])
        
        # Create item descriptions
        item_texts = []
        for item in items:
            if item_type == "hotel":
                item_text = f"{item.name} {item.description} {item.amenities} {item.city} {item.country}"
            elif item_type == "attraction":
                item_text = f"{item.name} {item.description} {item.category} {item.city} {item.country}"
            else:  # flight
                item_text = f"{item.airline} {item.origin} {item.destination} {item.flight_class}"
            item_texts.append(item_text)
        
        # Get item embeddings
        item_embeddings = model.encode(item_texts)
        
        # Calculate cosine similarity using numpy
        # Normalize embeddings
        user_norm = user_embedding / np.linalg.norm(user_embedding, axis=1, keepdims=True)
        items_norm = item_embeddings / np.linalg.norm(item_embeddings, axis=1, keepdims=True)
        # Calculate cosine similarity
        similarities = np.dot(user_norm, items_norm.T)[0]
        
        # Return items with similarity scores
        return list(zip(items, similarities))
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        # Fallback: return items with zero scores
        return [(item, 0.0) for item in items]

@app.post("/api/chat", response_model=RecommendationsResponse)
def chat_with_agent(message: ChatMessage, db: Session = Depends(get_db)):
    """Handle chatbot messages and update recommendations using sentence transformers and cosine similarity"""
    user_preferences = message.message
    
    # Parse original plan if provided
    if message.current_plan:
        parsed = parse_travel_plan(message.current_plan)
        original_locations = parsed["locations"]
        days = parsed["days"]
    else:
        original_locations = []
        days = 1
    
    # Extract locations from user message - these override the original plan locations
    message_locations = extract_locations(user_preferences)
    
    # Check if user mentioned a different number of days in the chat message
    chat_days = extract_days(user_preferences)
    if chat_days > 1:
        days = chat_days
    
    # If user mentioned locations in chatbot, use those (override original plan)
    # Otherwise, use original plan locations
    if message_locations:
        all_locations = message_locations
    else:
        all_locations = original_locations
    
    # Get base recommendations filtered by locations
    if all_locations:
        hotels = db.query(Hotel).filter(
            Hotel.city.in_(all_locations) | Hotel.country.in_(all_locations)
        ).all()
        
        flights = db.query(Flight).filter(
            Flight.destination.in_(all_locations) | Flight.origin.in_(all_locations)
        ).all()
        
        attractions = db.query(Attraction).filter(
            Attraction.city.in_(all_locations) | Attraction.country.in_(all_locations)
        ).all()
    else:
        # If no locations specified, get all items
        hotels = db.query(Hotel).all()
        flights = db.query(Flight).all()
        attractions = db.query(Attraction).all()

    # Calculate similarity scores using sentence transformers
    # Get hotels with similarity scores
    hotel_scores = calculate_similarity_scores(user_preferences, hotels, "hotel")
    # Sort by similarity score (descending) and take top 6
    hotel_scores.sort(key=lambda x: x[1], reverse=True)
    hotels = [h[0] for h in hotel_scores]

    # Get flights with similarity scores
    flight_scores = calculate_similarity_scores(user_preferences, flights, "flight")
    # Sort by similarity score (descending) and take top 5
    flight_scores.sort(key=lambda x: x[1], reverse=True)
    flights = [f[0] for f in flight_scores]
    
    # Get attractions with similarity scores
    attraction_scores = calculate_similarity_scores(user_preferences, attractions, "attraction")
    # Sort by similarity score (descending) and take top 6
    attraction_scores.sort(key=lambda x: x[1], reverse=True)
    attractions = [a[0] for a in attraction_scores]
        
    # except Exception as e:
    #     print(f"Error calculating similarity scores: {e}")
    #     # Fallback to simple filtering
    #     hotels = filter_by_preferences(hotels, user_preferences.lower())
    #     attractions = filter_by_preferences(attractions, user_preferences.lower())
    
    return RecommendationsResponse(
        hotels=[HotelResponse(**{k: getattr(h, k) for k in HotelResponse.__fields__.keys()}) for h in hotels],
        flights=[FlightResponse(**{k: getattr(f, k) for k in FlightResponse.__fields__.keys()}) for f in flights],
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

