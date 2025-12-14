from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import sqlite3
from datetime import datetime, timedelta
import random

Base = declarative_base()

class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)
    price_per_night = Column(Float)
    rating = Column(Float)
    description = Column(Text)
    amenities = Column(Text)  # JSON string
    image_url = Column(String)
    address = Column(String)

class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True)
    airline = Column(String)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    departure_date = Column(String)
    departure_time = Column(String)
    arrival_time = Column(String)
    price = Column(Float)
    duration = Column(String)
    stops = Column(Integer)
    flight_class = Column(String)

class Attraction(Base):
    __tablename__ = "attractions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)
    category = Column(String)  # nature, history, culture, etc.
    description = Column(Text)
    price = Column(Float)
    rating = Column(Float)
    image_url = Column(String)
    address = Column(String)
    opening_hours = Column(String)

# Database setup
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "travel_agent.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    populate_sample_data()

def populate_sample_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Hotel).count() > 0:
            return
        
        # Sample Hotels
        hotels_data = [
            {"name": "Tokyo Grand Hotel", "city": "Tokyo", "country": "Japan", "price_per_night": 150.0, "rating": 4.5, 
             "description": "Luxury hotel in the heart of Tokyo with modern amenities", 
             "amenities": "WiFi, Pool, Spa, Restaurant", "image_url": "https://via.placeholder.com/300", 
             "address": "1-1-1 Shibuya, Tokyo"},
            {"name": "Kyoto Traditional Inn", "city": "Kyoto", "country": "Japan", "price_per_night": 120.0, "rating": 4.7,
             "description": "Authentic Japanese ryokan experience", 
             "amenities": "WiFi, Onsen, Traditional Breakfast", "image_url": "https://via.placeholder.com/300",
             "address": "2-2-2 Gion, Kyoto"},
            {"name": "Hakone Mountain Resort", "city": "Hakone", "country": "Japan", "price_per_night": 200.0, "rating": 4.8,
             "description": "Scenic resort with hot springs and mountain views",
             "amenities": "WiFi, Onsen, Restaurant, Mountain Views", "image_url": "https://via.placeholder.com/300",
             "address": "3-3-3 Hakone, Kanagawa"},
            {"name": "Paris Eiffel View Hotel", "city": "Paris", "country": "France", "price_per_night": 180.0, "rating": 4.6,
             "description": "Boutique hotel with views of the Eiffel Tower",
             "amenities": "WiFi, Restaurant, City Views", "image_url": "https://via.placeholder.com/300",
             "address": "15 Rue de la Tour, Paris"},
            {"name": "Rome Historic Center Hotel", "city": "Rome", "country": "Italy", "price_per_night": 130.0, "rating": 4.4,
             "description": "Charming hotel near the Colosseum",
             "amenities": "WiFi, Breakfast, Historic Location", "image_url": "https://via.placeholder.com/300",
             "address": "Via dei Fori Imperiali, Rome"},
            {"name": "Barcelona Beach Hotel", "city": "Barcelona", "country": "Spain", "price_per_night": 140.0, "rating": 4.5,
             "description": "Modern hotel steps from the beach",
             "amenities": "WiFi, Pool, Beach Access, Restaurant", "image_url": "https://via.placeholder.com/300",
             "address": "Passeig de la Barceloneta, Barcelona"},
        ]
        
        for hotel in hotels_data:
            db.add(Hotel(**hotel))
        
        # Sample Flights
        flights_data = [
            {"airline": "Japan Airlines", "origin": "New York", "destination": "Tokyo", "departure_date": "2024-06-01",
             "departure_time": "10:00", "arrival_time": "14:30", "price": 1200.0, "duration": "14h 30m", "stops": 0, "flight_class": "Economy"},
            {"airline": "All Nippon Airways", "origin": "Los Angeles", "destination": "Tokyo", "departure_date": "2024-06-01",
             "departure_time": "11:00", "arrival_time": "15:45", "price": 1100.0, "duration": "12h 45m", "stops": 0, "flight_class": "Economy"},
            {"airline": "Shinkansen", "origin": "Tokyo", "destination": "Kyoto", "departure_date": "2024-06-04",
             "departure_time": "09:00", "arrival_time": "11:30", "price": 130.0, "duration": "2h 30m", "stops": 0, "flight_class": "Standard"},
            {"airline": "Air France", "origin": "New York", "destination": "Paris", "departure_date": "2024-07-01",
             "departure_time": "20:00", "arrival_time": "08:00", "price": 900.0, "duration": "7h 0m", "stops": 0, "flight_class": "Economy"},
            {"airline": "Lufthansa", "origin": "London", "destination": "Rome", "departure_date": "2024-07-05",
             "departure_time": "14:00", "arrival_time": "16:30", "price": 250.0, "duration": "2h 30m", "stops": 0, "flight_class": "Economy"},
        ]
        
        for flight in flights_data:
            db.add(Flight(**flight))
        
        # Sample Attractions
        attractions_data = [
            {"name": "Shibuya Crossing", "city": "Tokyo", "country": "Japan", "category": "culture",
             "description": "The world's busiest pedestrian crossing", "price": 0.0, "rating": 4.5,
             "image_url": "https://via.placeholder.com/300", "address": "Shibuya, Tokyo", "opening_hours": "24/7"},
            {"name": "Asakusa Temple", "city": "Tokyo", "country": "Japan", "category": "history",
             "description": "Historic Buddhist temple in Tokyo", "price": 0.0, "rating": 4.6,
             "image_url": "https://via.placeholder.com/300", "address": "2-3-1 Asakusa, Tokyo", "opening_hours": "6:00-17:00"},
            {"name": "Meiji Shrine", "city": "Tokyo", "country": "Japan", "category": "nature",
             "description": "Peaceful Shinto shrine surrounded by forest", "price": 0.0, "rating": 4.7,
             "image_url": "https://via.placeholder.com/300", "address": "1-1 Yoyogi Kamizono-cho, Tokyo", "opening_hours": "6:00-18:00"},
            {"name": "Hakone Open-Air Museum", "city": "Hakone", "country": "Japan", "category": "nature",
             "description": "Beautiful outdoor sculpture museum with mountain views", "price": 15.0, "rating": 4.8,
             "image_url": "https://via.placeholder.com/300", "address": "1121 Ninotaira, Hakone", "opening_hours": "9:00-17:00"},
            {"name": "Fushimi Inari Shrine", "city": "Kyoto", "country": "Japan", "category": "nature",
             "description": "Famous shrine with thousands of torii gates", "price": 0.0, "rating": 4.9,
             "image_url": "https://via.placeholder.com/300", "address": "68 Fukakusa Yabunouchicho, Kyoto", "opening_hours": "24/7"},
            {"name": "Eiffel Tower", "city": "Paris", "country": "France", "category": "culture",
             "description": "Iconic iron lattice tower", "price": 25.0, "rating": 4.7,
             "image_url": "https://via.placeholder.com/300", "address": "Champ de Mars, Paris", "opening_hours": "9:00-23:00"},
            {"name": "Louvre Museum", "city": "Paris", "country": "France", "category": "history",
             "description": "World's largest art museum", "price": 17.0, "rating": 4.8,
             "image_url": "https://via.placeholder.com/300", "address": "Rue de Rivoli, Paris", "opening_hours": "9:00-18:00"},
            {"name": "Colosseum", "city": "Rome", "country": "Italy", "category": "history",
             "description": "Ancient Roman amphitheater", "price": 16.0, "rating": 4.6,
             "image_url": "https://via.placeholder.com/300", "address": "Piazza del Colosseo, Rome", "opening_hours": "8:30-19:00"},
            {"name": "Sagrada Familia", "city": "Barcelona", "country": "Spain", "category": "culture",
             "description": "Gaudi's masterpiece basilica", "price": 20.0, "rating": 4.9,
             "image_url": "https://via.placeholder.com/300", "address": "Carrer de Mallorca, Barcelona", "opening_hours": "9:00-20:00"},
        ]
        
        for attraction in attractions_data:
            db.add(Attraction(**attraction))
        
        db.commit()
    except Exception as e:
        print(f"Error populating data: {e}")
        db.rollback()
    finally:
        db.close()

