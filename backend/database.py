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
    booking_link = Column(String)
    images = Column(Text)  # JSON string of image URLs

class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True)
    airline = Column(String)
    flight_number = Column(String)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    departure_airport = Column(String)
    arrival_airport = Column(String)
    departure_date = Column(String)
    departure_time = Column(String)
    arrival_time = Column(String)
    price = Column(Float)
    duration = Column(String)
    stops = Column(Integer)
    flight_class = Column(String)
    booking_link = Column(String)

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
    ticket_link = Column(String)
    images = Column(Text)  # JSON string of image URLs

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
        # Check if data already exists and has the new columns
        try:
            # Try to query a hotel with new fields to check if schema is updated
            test_hotel = db.query(Hotel).first()
            if test_hotel and hasattr(test_hotel, 'booking_link') and test_hotel.booking_link is not None:
                # Schema is updated and data exists
                return
        except Exception:
            # Schema mismatch - need to repopulate
            pass
        
        # Clear existing data if schema changed
        db.query(Hotel).delete()
        db.query(Flight).delete()
        db.query(Attraction).delete()
        db.commit()
        
        import json
        
        # 20 Hotels
        hotels_data = [
            {"name": "Tokyo Grand Hotel", "city": "Tokyo", "country": "Japan", "price_per_night": 150.0, "rating": 4.5, 
             "description": "Luxury hotel in the heart of Tokyo with modern amenities and stunning city views", 
             "amenities": "WiFi, Pool, Spa, Restaurant, Fitness Center, Business Center", 
             "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&h=300&fit=crop",
             "address": "1-1-1 Shibuya, Shibuya City, Tokyo 150-0002, Japan",
             "booking_link": "https://booking.com/tokyo-grand-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800", "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Kyoto Traditional Inn", "city": "Kyoto", "country": "Japan", "price_per_night": 120.0, "rating": 4.7,
             "description": "Authentic Japanese ryokan experience with traditional tatami rooms and kaiseki dining", 
             "amenities": "WiFi, Onsen, Traditional Breakfast, Garden, Tea Ceremony", 
             "image_url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400&h=300&fit=crop",
             "address": "2-2-2 Gion, Higashiyama Ward, Kyoto 605-0073, Japan",
             "booking_link": "https://booking.com/kyoto-traditional-inn",
             "images": json.dumps(["https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800", "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800"])},
            {"name": "Hakone Mountain Resort", "city": "Hakone", "country": "Japan", "price_per_night": 200.0, "rating": 4.8,
             "description": "Scenic resort with hot springs, mountain views, and luxurious accommodations",
             "amenities": "WiFi, Onsen, Restaurant, Mountain Views, Spa, Hiking Trails",
             "image_url": "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400&h=300&fit=crop",
             "address": "3-3-3 Hakone, Ashigarashimo District, Kanagawa 250-0522, Japan",
             "booking_link": "https://booking.com/hakone-mountain-resort",
             "images": json.dumps(["https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800"])},
            {"name": "Paris Eiffel View Hotel", "city": "Paris", "country": "France", "price_per_night": 180.0, "rating": 4.6,
             "description": "Boutique hotel with breathtaking views of the Eiffel Tower and elegant Parisian decor",
             "amenities": "WiFi, Restaurant, City Views, Rooftop Terrace, Concierge",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "15 Rue de la Tour, 75016 Paris, France",
             "booking_link": "https://booking.com/paris-eiffel-view-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800", "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=800"])},
            {"name": "Rome Historic Center Hotel", "city": "Rome", "country": "Italy", "price_per_night": 130.0, "rating": 4.4,
             "description": "Charming hotel near the Colosseum with classic Italian architecture and warm hospitality",
             "amenities": "WiFi, Breakfast, Historic Location, Air Conditioning, Bar",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Via dei Fori Imperiali, 00184 Rome, Italy",
             "booking_link": "https://booking.com/rome-historic-center-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800", "https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=800"])},
            {"name": "Barcelona Beach Hotel", "city": "Barcelona", "country": "Spain", "price_per_night": 140.0, "rating": 4.5,
             "description": "Modern hotel steps from the beach with contemporary design and Mediterranean vibes",
             "amenities": "WiFi, Pool, Beach Access, Restaurant, Rooftop Bar, Bike Rental",
             "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400&h=300&fit=crop",
             "address": "Passeig de la Barceloneta, 08003 Barcelona, Spain",
             "booking_link": "https://booking.com/barcelona-beach-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800", "https://images.unsplash.com/photo-1539650116574-75c0c6d73a6e?w=800"])},
            {"name": "London Thames View Hotel", "city": "London", "country": "UK", "price_per_night": 160.0, "rating": 4.6,
             "description": "Elegant hotel overlooking the Thames with classic British charm and modern amenities",
             "amenities": "WiFi, Restaurant, River Views, Afternoon Tea, Fitness Center",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Thames Embankment, London SW1A 2HH, UK",
             "booking_link": "https://booking.com/london-thames-view-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Berlin Modern Hotel", "city": "Berlin", "country": "Germany", "price_per_night": 110.0, "rating": 4.3,
             "description": "Contemporary design hotel in the heart of Berlin with vibrant art scene",
             "amenities": "WiFi, Restaurant, Bar, Bike Rental, Art Gallery",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Unter den Linden, 10117 Berlin, Germany",
             "booking_link": "https://booking.com/berlin-modern-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Amsterdam Canal House", "city": "Amsterdam", "country": "Netherlands", "price_per_night": 145.0, "rating": 4.7,
             "description": "Historic canal house converted into boutique hotel with Dutch character",
             "amenities": "WiFi, Breakfast, Canal Views, Bike Rental, Wine Bar",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Prinsengracht, 1016 Amsterdam, Netherlands",
             "booking_link": "https://booking.com/amsterdam-canal-house",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Vienna Imperial Hotel", "city": "Vienna", "country": "Austria", "price_per_night": 170.0, "rating": 4.8,
             "description": "Grand imperial hotel with opulent decor and world-class service",
             "amenities": "WiFi, Spa, Fine Dining, Concierge, Ballroom, Library",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Ringstraße, 1010 Vienna, Austria",
             "booking_link": "https://booking.com/vienna-imperial-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Prague Castle View Hotel", "city": "Prague", "country": "Czech Republic", "price_per_night": 95.0, "rating": 4.5,
             "description": "Charming hotel with views of Prague Castle and historic Old Town",
             "amenities": "WiFi, Breakfast, Castle Views, Restaurant, Bar",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Malá Strana, 118 00 Prague, Czech Republic",
             "booking_link": "https://booking.com/prague-castle-view-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Dubai Marina Hotel", "city": "Dubai", "country": "UAE", "price_per_night": 220.0, "rating": 4.9,
             "description": "Ultra-modern luxury hotel with stunning marina views and world-class amenities",
             "amenities": "WiFi, Infinity Pool, Spa, Multiple Restaurants, Sky Bar, Beach Access",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Dubai Marina, Dubai, UAE",
             "booking_link": "https://booking.com/dubai-marina-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Singapore Marina Bay Hotel", "city": "Singapore", "country": "Singapore", "price_per_night": 250.0, "rating": 4.8,
             "description": "Iconic hotel with infinity pool overlooking Marina Bay and city skyline",
             "amenities": "WiFi, Infinity Pool, Spa, Casino, Multiple Restaurants, Rooftop Bar",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "10 Bayfront Avenue, Singapore 018956",
             "booking_link": "https://booking.com/singapore-marina-bay-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Bangkok Riverside Hotel", "city": "Bangkok", "country": "Thailand", "price_per_night": 80.0, "rating": 4.4,
             "description": "Modern hotel along the Chao Phraya River with traditional Thai hospitality",
             "amenities": "WiFi, Pool, Spa, River Views, Thai Restaurant, Rooftop Bar",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Charoen Krung Road, Bangkok 10500, Thailand",
             "booking_link": "https://booking.com/bangkok-riverside-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Sydney Harbour Hotel", "city": "Sydney", "country": "Australia", "price_per_night": 190.0, "rating": 4.7,
             "description": "Luxury hotel with panoramic views of Sydney Harbour and Opera House",
             "amenities": "WiFi, Pool, Spa, Harbour Views, Fine Dining, Rooftop Bar",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Circular Quay, Sydney NSW 2000, Australia",
             "booking_link": "https://booking.com/sydney-harbour-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "New York Times Square Hotel", "city": "New York", "country": "USA", "price_per_night": 200.0, "rating": 4.5,
             "description": "Bustling hotel in the heart of Times Square with vibrant energy",
             "amenities": "WiFi, Fitness Center, Restaurant, Bar, Business Center, Concierge",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Times Square, New York, NY 10036, USA",
             "booking_link": "https://booking.com/new-york-times-square-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Los Angeles Beach Resort", "city": "Los Angeles", "country": "USA", "price_per_night": 180.0, "rating": 4.6,
             "description": "Beachfront resort with Pacific Ocean views and California cool vibes",
             "amenities": "WiFi, Beach Access, Pool, Spa, Beach Bar, Restaurant, Fitness Center",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Santa Monica Beach, Los Angeles, CA 90401, USA",
             "booking_link": "https://booking.com/los-angeles-beach-resort",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Istanbul Bosphorus Hotel", "city": "Istanbul", "country": "Turkey", "price_per_night": 125.0, "rating": 4.6,
             "description": "Historic hotel overlooking the Bosphorus with blend of European and Asian cultures",
             "amenities": "WiFi, Bosphorus Views, Turkish Bath, Restaurant, Rooftop Terrace",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Bosphorus, 34420 Istanbul, Turkey",
             "booking_link": "https://booking.com/istanbul-bosphorus-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Cairo Nile View Hotel", "city": "Cairo", "country": "Egypt", "price_per_night": 100.0, "rating": 4.4,
             "description": "Luxury hotel on the banks of the Nile with views of ancient pyramids",
             "amenities": "WiFi, Pool, Nile Views, Spa, Egyptian Restaurant, Rooftop Bar",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Nile Corniche, Cairo, Egypt",
             "booking_link": "https://booking.com/cairo-nile-view-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Rio Copacabana Hotel", "city": "Rio de Janeiro", "country": "Brazil", "price_per_night": 135.0, "rating": 4.5,
             "description": "Vibrant beachfront hotel on famous Copacabana Beach with samba vibes",
             "amenities": "WiFi, Beach Access, Pool, Beach Bar, Restaurant, Fitness Center",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Avenida Atlântica, Copacabana, Rio de Janeiro, Brazil",
             "booking_link": "https://booking.com/rio-copacabana-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Buenos Aires Tango Hotel", "city": "Buenos Aires", "country": "Argentina", "price_per_night": 110.0, "rating": 4.3,
             "description": "Boutique hotel in historic San Telmo with tango shows and Argentine charm",
             "amenities": "WiFi, Tango Shows, Restaurant, Bar, Rooftop Terrace",
             "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "San Telmo, Buenos Aires, Argentina",
             "booking_link": "https://booking.com/buenos-aires-tango-hotel",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
        ]
        
        for hotel in hotels_data:
            db.add(Hotel(**hotel))
        
        # 20 Flights
        flights_data = [
            {"airline": "Japan Airlines", "flight_number": "JL004", "origin": "New York", "destination": "Tokyo",
             "departure_airport": "John F. Kennedy International Airport (JFK)", "arrival_airport": "Narita International Airport (NRT)",
             "departure_date": "2024-06-01", "departure_time": "10:00", "arrival_time": "14:30+1", "price": 1200.0, 
             "duration": "14h 30m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://japanairlines.com/book/JL004"},
            {"airline": "All Nippon Airways", "flight_number": "NH106", "origin": "Los Angeles", "destination": "Tokyo",
             "departure_airport": "Los Angeles International Airport (LAX)", "arrival_airport": "Narita International Airport (NRT)",
             "departure_date": "2024-06-01", "departure_time": "11:00", "arrival_time": "15:45+1", "price": 1100.0, 
             "duration": "12h 45m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://ana.co.jp/book/NH106"},
            {"airline": "Shinkansen", "flight_number": "NOZOMI 1", "origin": "Tokyo", "destination": "Kyoto",
             "departure_airport": "Tokyo Station", "arrival_airport": "Kyoto Station",
             "departure_date": "2024-06-04", "departure_time": "09:00", "arrival_time": "11:30", "price": 130.0, 
             "duration": "2h 30m", "stops": 0, "flight_class": "Standard",
             "booking_link": "https://jr-central.co.jp/book/NOZOMI1"},
            {"airline": "Air France", "flight_number": "AF007", "origin": "New York", "destination": "Paris",
             "departure_airport": "John F. Kennedy International Airport (JFK)", "arrival_airport": "Charles de Gaulle Airport (CDG)",
             "departure_date": "2024-07-01", "departure_time": "20:00", "arrival_time": "08:00+1", "price": 900.0, 
             "duration": "7h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://airfrance.com/book/AF007"},
            {"airline": "Lufthansa", "flight_number": "LH440", "origin": "London", "destination": "Rome",
             "departure_airport": "Heathrow Airport (LHR)", "arrival_airport": "Leonardo da Vinci Airport (FCO)",
             "departure_date": "2024-07-05", "departure_time": "14:00", "arrival_time": "16:30", "price": 250.0, 
             "duration": "2h 30m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://lufthansa.com/book/LH440"},
            {"airline": "British Airways", "flight_number": "BA268", "origin": "New York", "destination": "London",
             "departure_airport": "John F. Kennedy International Airport (JFK)", "arrival_airport": "Heathrow Airport (LHR)",
             "departure_date": "2024-07-10", "departure_time": "22:00", "arrival_time": "10:00+1", "price": 850.0, 
             "duration": "7h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://britishairways.com/book/BA268"},
            {"airline": "Emirates", "flight_number": "EK201", "origin": "New York", "destination": "Dubai",
             "departure_airport": "John F. Kennedy International Airport (JFK)", "arrival_airport": "Dubai International Airport (DXB)",
             "departure_date": "2024-07-15", "departure_time": "22:30", "arrival_time": "19:30+1", "price": 1100.0, 
             "duration": "13h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://emirates.com/book/EK201"},
            {"airline": "Singapore Airlines", "flight_number": "SQ21", "origin": "New York", "destination": "Singapore",
             "departure_airport": "John F. Kennedy International Airport (JFK)", "arrival_airport": "Changi Airport (SIN)",
             "departure_date": "2024-07-20", "departure_time": "23:00", "arrival_time": "06:00+2", "price": 1400.0, 
             "duration": "18h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://singaporeair.com/book/SQ21"},
            {"airline": "Qantas", "flight_number": "QF12", "origin": "Los Angeles", "destination": "Sydney",
             "departure_airport": "Los Angeles International Airport (LAX)", "arrival_airport": "Sydney Airport (SYD)",
             "departure_date": "2024-08-01", "departure_time": "22:00", "arrival_time": "07:00+2", "price": 1300.0, 
             "duration": "14h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://qantas.com/book/QF12"},
            {"airline": "Turkish Airlines", "flight_number": "TK1", "origin": "New York", "destination": "Istanbul",
             "departure_airport": "John F. Kennedy International Airport (JFK)", "arrival_airport": "Istanbul Airport (IST)",
             "departure_date": "2024-08-05", "departure_time": "23:30", "arrival_time": "16:30+1", "price": 950.0, 
             "duration": "10h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://turkishairlines.com/book/TK1"},
            {"airline": "KLM", "flight_number": "KL642", "origin": "Amsterdam", "destination": "Bangkok",
             "departure_airport": "Amsterdam Airport Schiphol (AMS)", "arrival_airport": "Suvarnabhumi Airport (BKK)",
             "departure_date": "2024-08-10", "departure_time": "12:00", "arrival_time": "05:30+1", "price": 800.0, 
             "duration": "11h 30m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://klm.com/book/KL642"},
            {"airline": "Lufthansa", "flight_number": "LH441", "origin": "Frankfurt", "destination": "Barcelona",
             "departure_airport": "Frankfurt Airport (FRA)", "arrival_airport": "Barcelona-El Prat Airport (BCN)",
             "departure_date": "2024-08-15", "departure_time": "10:00", "arrival_time": "12:00", "price": 180.0, 
             "duration": "2h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://lufthansa.com/book/LH441"},
            {"airline": "Ryanair", "flight_number": "FR1234", "origin": "London", "destination": "Rome",
             "departure_airport": "Stansted Airport (STN)", "arrival_airport": "Ciampino Airport (CIA)",
             "departure_date": "2024-08-20", "departure_time": "08:00", "arrival_time": "11:30", "price": 120.0, 
             "duration": "2h 30m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://ryanair.com/book/FR1234"},
            {"airline": "EasyJet", "flight_number": "U21456", "origin": "Paris", "destination": "Barcelona",
             "departure_airport": "Charles de Gaulle Airport (CDG)", "arrival_airport": "Barcelona-El Prat Airport (BCN)",
             "departure_date": "2024-08-25", "departure_time": "14:00", "arrival_time": "15:30", "price": 100.0, 
             "duration": "1h 30m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://easyjet.com/book/U21456"},
            {"airline": "Delta Air Lines", "flight_number": "DL200", "origin": "New York", "destination": "Los Angeles",
             "departure_airport": "John F. Kennedy International Airport (JFK)", "arrival_airport": "Los Angeles International Airport (LAX)",
             "departure_date": "2024-09-01", "departure_time": "08:00", "arrival_time": "11:30", "price": 400.0, 
             "duration": "5h 30m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://delta.com/book/DL200"},
            {"airline": "United Airlines", "flight_number": "UA100", "origin": "San Francisco", "destination": "Tokyo",
             "departure_airport": "San Francisco International Airport (SFO)", "arrival_airport": "Narita International Airport (NRT)",
             "departure_date": "2024-09-05", "departure_time": "11:00", "arrival_time": "15:00+1", "price": 1150.0, 
             "duration": "11h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://united.com/book/UA100"},
            {"airline": "American Airlines", "flight_number": "AA100", "origin": "Miami", "destination": "Rio de Janeiro",
             "departure_airport": "Miami International Airport (MIA)", "arrival_airport": "Galeão International Airport (GIG)",
             "departure_date": "2024-09-10", "departure_time": "22:00", "arrival_time": "08:00+1", "price": 750.0, 
             "duration": "8h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://aa.com/book/AA100"},
            {"airline": "EgyptAir", "flight_number": "MS777", "origin": "Cairo", "destination": "Dubai",
             "departure_airport": "Cairo International Airport (CAI)", "arrival_airport": "Dubai International Airport (DXB)",
             "departure_date": "2024-09-15", "departure_time": "10:00", "arrival_time": "14:00", "price": 350.0, 
             "duration": "3h 0m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://egyptair.com/book/MS777"},
            {"airline": "Qatar Airways", "flight_number": "QR815", "origin": "Doha", "destination": "Bangkok",
             "departure_airport": "Hamad International Airport (DOH)", "arrival_airport": "Suvarnabhumi Airport (BKK)",
             "departure_date": "2024-09-20", "departure_time": "02:00", "arrival_time": "08:30", "price": 450.0, 
             "duration": "6h 30m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://qatarairways.com/book/QR815"},
            {"airline": "Aer Lingus", "flight_number": "EI101", "origin": "Dublin", "destination": "New York",
             "departure_airport": "Dublin Airport (DUB)", "arrival_airport": "John F. Kennedy International Airport (JFK)",
             "departure_date": "2024-09-25", "departure_time": "13:00", "arrival_time": "15:30", "price": 650.0, 
             "duration": "7h 30m", "stops": 0, "flight_class": "Economy",
             "booking_link": "https://aerlingus.com/book/EI101"},
        ]
        
        for flight in flights_data:
            db.add(Flight(**flight))
        
        # 20 Tourist Attractions
        attractions_data = [
            {"name": "Shibuya Crossing", "city": "Tokyo", "country": "Japan", "category": "culture",
             "description": "The world's busiest pedestrian crossing, a symbol of modern Tokyo with thousands crossing daily",
             "price": 0.0, "rating": 4.5, "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=300&fit=crop",
             "address": "Shibuya, Shibuya City, Tokyo 150-0002, Japan", "opening_hours": "24/7",
             "ticket_link": "https://tokyo-tourism.com/shibuya-crossing",
             "images": json.dumps(["https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800", "https://images.unsplash.com/photo-1528164344705-47542687000d?w=800"])},
            {"name": "Asakusa Temple (Senso-ji)", "city": "Tokyo", "country": "Japan", "category": "history",
             "description": "Historic Buddhist temple in Tokyo, the oldest temple in the city dating back to 628 AD",
             "price": 0.0, "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1528164344705-47542687000d?w=400&h=300&fit=crop",
             "address": "2-3-1 Asakusa, Taito City, Tokyo 111-0032, Japan", "opening_hours": "6:00-17:00",
             "ticket_link": "https://tokyo-tourism.com/asakusa-temple",
             "images": json.dumps(["https://images.unsplash.com/photo-1528164344705-47542687000d?w=800"])},
            {"name": "Meiji Shrine", "city": "Tokyo", "country": "Japan", "category": "nature",
             "description": "Peaceful Shinto shrine surrounded by forest in the heart of Tokyo, dedicated to Emperor Meiji",
             "price": 0.0, "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400&h=300&fit=crop",
             "address": "1-1 Yoyogi Kamizono-cho, Shibuya City, Tokyo 151-8557, Japan", "opening_hours": "6:00-18:00",
             "ticket_link": "https://tokyo-tourism.com/meiji-shrine",
             "images": json.dumps(["https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800"])},
            {"name": "Hakone Open-Air Museum", "city": "Hakone", "country": "Japan", "category": "nature",
             "description": "Beautiful outdoor sculpture museum with mountain views, featuring works by Picasso and Rodin",
             "price": 15.0, "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
             "address": "1121 Ninotaira, Hakone, Ashigarashimo District, Kanagawa 250-0407, Japan", "opening_hours": "9:00-17:00",
             "ticket_link": "https://hakone-museum.com/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800"])},
            {"name": "Fushimi Inari Shrine", "city": "Kyoto", "country": "Japan", "category": "nature",
             "description": "Famous shrine with thousands of vermillion torii gates forming tunnels up the mountain",
             "price": 0.0, "rating": 4.9, "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400&h=300&fit=crop",
             "address": "68 Fukakusa Yabunouchicho, Fushimi Ward, Kyoto 612-0882, Japan", "opening_hours": "24/7",
             "ticket_link": "https://kyoto-tourism.com/fushimi-inari",
             "images": json.dumps(["https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800"])},
            {"name": "Eiffel Tower", "city": "Paris", "country": "France", "category": "culture",
             "description": "Iconic iron lattice tower, symbol of Paris and one of the most recognized structures in the world",
             "price": 25.0, "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=400&h=300&fit=crop",
             "address": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France", "opening_hours": "9:00-23:00",
             "ticket_link": "https://toureiffel.paris/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=800"])},
            {"name": "Louvre Museum", "city": "Paris", "country": "France", "category": "history",
             "description": "World's largest art museum, home to the Mona Lisa and thousands of other masterpieces",
             "price": 17.0, "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1592229505726-ca121723b8ef?w=400&h=300&fit=crop",
             "address": "Rue de Rivoli, 75001 Paris, France", "opening_hours": "9:00-18:00",
             "ticket_link": "https://louvre.fr/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1592229505726-ca121723b8ef?w=800"])},
            {"name": "Colosseum", "city": "Rome", "country": "Italy", "category": "history",
             "description": "Ancient Roman amphitheater, the largest ever built, symbol of the Roman Empire",
             "price": 16.0, "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=400&h=300&fit=crop",
             "address": "Piazza del Colosseo, 1, 00184 Rome, Italy", "opening_hours": "8:30-19:00",
             "ticket_link": "https://colosseo.it/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=800"])},
            {"name": "Sagrada Familia", "city": "Barcelona", "country": "Spain", "category": "culture",
             "description": "Gaudi's masterpiece basilica, an unfinished architectural wonder with stunning organic designs",
             "price": 20.0, "rating": 4.9, "image_url": "https://images.unsplash.com/photo-1539650116574-75c0c6d73a6e?w=400&h=300&fit=crop",
             "address": "Carrer de Mallorca, 401, 08013 Barcelona, Spain", "opening_hours": "9:00-20:00",
             "ticket_link": "https://sagradafamilia.org/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1539650116574-75c0c6d73a6e?w=800"])},
            {"name": "Big Ben", "city": "London", "country": "UK", "category": "culture",
             "description": "Iconic clock tower and symbol of London, part of the Palace of Westminster",
             "price": 0.0, "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Westminster, London SW1A 0AA, UK", "opening_hours": "24/7",
             "ticket_link": "https://parliament.uk/visit",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Brandenburg Gate", "city": "Berlin", "country": "Germany", "category": "history",
             "description": "Neoclassical monument and symbol of German unity, located in the heart of Berlin",
             "price": 0.0, "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Pariser Platz, 10117 Berlin, Germany", "opening_hours": "24/7",
             "ticket_link": "https://berlin-tourism.com/brandenburg-gate",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Anne Frank House", "city": "Amsterdam", "country": "Netherlands", "category": "history",
             "description": "Museum dedicated to Jewish wartime diarist Anne Frank, located in the house where she hid",
             "price": 12.0, "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Westermarkt 20, 1016 GV Amsterdam, Netherlands", "opening_hours": "9:00-22:00",
             "ticket_link": "https://annefrank.org/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Schönbrunn Palace", "city": "Vienna", "country": "Austria", "category": "history",
             "description": "Former imperial summer residence with baroque architecture and beautiful gardens",
             "price": 18.0, "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Schönbrunn Schloßstraße 47, 1130 Vienna, Austria", "opening_hours": "8:00-17:30",
             "ticket_link": "https://schoenbrunn.at/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Charles Bridge", "city": "Prague", "country": "Czech Republic", "category": "culture",
             "description": "Historic stone bridge over the Vltava River, adorned with 30 baroque statues",
             "price": 0.0, "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Karlův most, 110 00 Prague, Czech Republic", "opening_hours": "24/7",
             "ticket_link": "https://prague-tourism.com/charles-bridge",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Burj Khalifa", "city": "Dubai", "country": "UAE", "category": "culture",
             "description": "World's tallest building at 828 meters, with observation decks offering stunning city views",
             "price": 35.0, "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "1 Sheikh Mohammed bin Rashid Blvd, Dubai, UAE", "opening_hours": "8:30-23:00",
             "ticket_link": "https://burjkhalifa.ae/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Gardens by the Bay", "city": "Singapore", "country": "Singapore", "category": "nature",
             "description": "Futuristic nature park with supertrees, cloud forest, and flower dome conservatories",
             "price": 28.0, "rating": 4.9, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "18 Marina Gardens Dr, Singapore 018953", "opening_hours": "5:00-2:00",
             "ticket_link": "https://gardensbythebay.com.sg/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Grand Palace", "city": "Bangkok", "country": "Thailand", "category": "history",
             "description": "Former royal residence with stunning Thai architecture and the sacred Temple of the Emerald Buddha",
             "price": 15.0, "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Na Phra Lan Rd, Phra Borom Maha Ratchawang, Phra Nakhon, Bangkok 10200, Thailand", "opening_hours": "8:30-15:30",
             "ticket_link": "https://royalgrandpalace.th/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Sydney Opera House", "city": "Sydney", "country": "Australia", "category": "culture",
             "description": "Iconic performing arts center with distinctive shell-like architecture on Sydney Harbour",
             "price": 43.0, "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Bennelong Point, Sydney NSW 2000, Australia", "opening_hours": "9:00-17:00",
             "ticket_link": "https://sydneyoperahouse.com/tours",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Statue of Liberty", "city": "New York", "country": "USA", "category": "culture",
             "description": "Iconic symbol of freedom and democracy, gift from France to the United States",
             "price": 24.0, "rating": 4.7, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Liberty Island, New York, NY 10004, USA", "opening_hours": "8:30-16:00",
             "ticket_link": "https://statueofliberty.org/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Pyramids of Giza", "city": "Cairo", "country": "Egypt", "category": "history",
             "description": "Ancient wonder of the world, including the Great Pyramid and the Sphinx",
             "price": 20.0, "rating": 4.6, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Al Haram, Giza Governorate, Egypt", "opening_hours": "8:00-17:00",
             "ticket_link": "https://egypt-tourism.com/pyramids-tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
            {"name": "Christ the Redeemer", "city": "Rio de Janeiro", "country": "Brazil", "category": "culture",
             "description": "Iconic Art Deco statue of Jesus Christ overlooking Rio from Corcovado Mountain",
             "price": 25.0, "rating": 4.8, "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&h=300&fit=crop",
             "address": "Parque Nacional da Tijuca, Rio de Janeiro, Brazil", "opening_hours": "8:00-19:00",
             "ticket_link": "https://cristoredentoroficial.com.br/en/tickets",
             "images": json.dumps(["https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"])},
        ]
        
        for attraction in attractions_data:
            db.add(Attraction(**attraction))
        
        db.commit()
    except Exception as e:
        print(f"Error populating data: {e}")
        db.rollback()
    finally:
        db.close()

