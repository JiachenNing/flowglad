export interface Hotel {
  id: number;
  name: string;
  city: string;
  country: string;
  price_per_night: number;
  rating: number;
  description: string;
  amenities: string;
  image_url: string;
  address: string;
}

export interface Flight {
  id: number;
  airline: string;
  origin: string;
  destination: string;
  departure_date: string;
  departure_time: string;
  arrival_time: string;
  price: number;
  duration: string;
  stops: number;
  flight_class: string;
}

export interface Attraction {
  id: number;
  name: string;
  city: string;
  country: string;
  category: string;
  description: string;
  price: number;
  rating: number;
  image_url: string;
  address: string;
  opening_hours: string;
}

export interface Recommendations {
  hotels: Hotel[];
  flights: Flight[];
  attractions: Attraction[];
  days: number;
  current_day: number;
}

export interface BookingResponse {
  success: boolean;
  message: string;
  booking_id?: string;
}
