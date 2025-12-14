from pydantic import BaseModel
from typing import List, Optional

class TravelPlanRequest(BaseModel):
    plan: str
    preferences: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    current_plan: Optional[str] = None

class HotelResponse(BaseModel):
    id: int
    name: str
    city: str
    country: str
    price_per_night: float
    rating: float
    description: str
    amenities: str
    image_url: str
    address: str
    booking_link: Optional[str] = None
    images: Optional[str] = None

class FlightResponse(BaseModel):
    id: int
    airline: str
    flight_number: Optional[str] = None
    origin: str
    destination: str
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    departure_date: str
    departure_time: str
    arrival_time: str
    price: float
    duration: str
    stops: int
    flight_class: str
    booking_link: Optional[str] = None

class AttractionResponse(BaseModel):
    id: int
    name: str
    city: str
    country: str
    category: str
    description: str
    price: float
    rating: float
    image_url: str
    address: str
    opening_hours: str
    ticket_link: Optional[str] = None
    images: Optional[str] = None

class RecommendationsResponse(BaseModel):
    hotels: List[HotelResponse]
    flights: List[FlightResponse]
    attractions: List[AttractionResponse]
    days: int = 1
    current_day: int = 1

class BookingRequest(BaseModel):
    type: str  # hotel, flight, or attraction
    id: int
    date: Optional[str] = None

class BookingResponse(BaseModel):
    success: bool
    message: str
    booking_id: Optional[str] = None

