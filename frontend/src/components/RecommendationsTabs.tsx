import { useState } from 'react';
import type { Hotel, Flight, Attraction } from '../types';
import { api } from '../api';
import './RecommendationsTabs.css';

interface RecommendationsTabsProps {
  hotels: Hotel[];
  flights: Flight[];
  attractions: Attraction[];
  days: number;
  currentDay: number;
  onDayChange: (day: number) => void;
}

export default function RecommendationsTabs({
  hotels,
  flights,
  attractions,
  days,
  currentDay,
  onDayChange
}: RecommendationsTabsProps) {
  const [activeTab, setActiveTab] = useState<'hotels' | 'flights' | 'attractions'>('hotels');
  const [selectedItem, setSelectedItem] = useState<{ type: string; item: Hotel | Flight | Attraction } | null>(null);
  const [bookingSuccess, setBookingSuccess] = useState<string | null>(null);

  const handleBook = async (type: 'hotel' | 'flight' | 'attraction', id: number) => {
    try {
      const result = await api.bookItem(type, id);
      setBookingSuccess(result.message);
      setTimeout(() => {
        setBookingSuccess(null);
        setSelectedItem(null);
      }, 3000);
    } catch (error) {
      alert('Booking failed. Please try again.');
    }
  };

  const renderItem = (item: Hotel | Flight | Attraction, type: 'hotel' | 'flight' | 'attraction') => {
    return (
      <div key={item.id} className="recommendation-card" onClick={() => setSelectedItem({ type, item })}>
        {type === 'hotel' && (
          <>
            <img src={(item as Hotel).image_url} alt={(item as Hotel).name} />
            <div className="card-content">
              <h3>{(item as Hotel).name}</h3>
              <p className="location">{(item as Hotel).city}, {(item as Hotel).country}</p>
              <p className="description">{(item as Hotel).description}</p>
              <div className="card-footer">
                <span className="rating">⭐ {(item as Hotel).rating}</span>
                <span className="price">${(item as Hotel).price_per_night}/night</span>
              </div>
            </div>
          </>
        )}
        {type === 'flight' && (
          <>
            <div className="card-content">
              <h3>{(item as Flight).airline}</h3>
              <p className="route">{(item as Flight).origin} → {(item as Flight).destination}</p>
              <p className="time">{(item as Flight).departure_time} - {(item as Flight).arrival_time}</p>
              <p className="duration">Duration: {(item as Flight).duration}</p>
              <div className="card-footer">
                <span className="stops">{(item as Flight).stops} stops</span>
                <span className="price">${(item as Flight).price}</span>
              </div>
            </div>
          </>
        )}
        {type === 'attraction' && (
          <>
            <img src={(item as Attraction).image_url} alt={(item as Attraction).name} />
            <div className="card-content">
              <h3>{(item as Attraction).name}</h3>
              <p className="location">{(item as Attraction).city}, {(item as Attraction).country}</p>
              <p className="category">{(item as Attraction).category}</p>
              <p className="description">{(item as Attraction).description}</p>
              <div className="card-footer">
                <span className="rating">⭐ {(item as Attraction).rating}</span>
                <span className="price">${(item as Attraction).price === 0 ? 'Free' : (item as Attraction).price}</span>
              </div>
            </div>
          </>
        )}
      </div>
    );
  };

  return (
    <div className="recommendations-container">
      {days > 1 && (
        <div className="day-navigation">
          <button
            onClick={() => onDayChange(Math.max(1, currentDay - 1))}
            disabled={currentDay === 1}
          >
            Previous Day
          </button>
          <span>Day {currentDay} of {days}</span>
          <button
            onClick={() => onDayChange(Math.min(days, currentDay + 1))}
            disabled={currentDay === days}
          >
            Next Day
          </button>
        </div>
      )}

      <div className="tabs">
        <button
          className={activeTab === 'hotels' ? 'active' : ''}
          onClick={() => setActiveTab('hotels')}
        >
          Hotels ({hotels.length})
        </button>
        <button
          className={activeTab === 'flights' ? 'active' : ''}
          onClick={() => setActiveTab('flights')}
        >
          Flights ({flights.length})
        </button>
        <button
          className={activeTab === 'attractions' ? 'active' : ''}
          onClick={() => setActiveTab('attractions')}
        >
          Attractions ({attractions.length})
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'hotels' && (
          <div className="recommendations-grid">
            {hotels.map(hotel => renderItem(hotel, 'hotel'))}
          </div>
        )}
        {activeTab === 'flights' && (
          <div className="recommendations-grid">
            {flights.map(flight => renderItem(flight, 'flight'))}
          </div>
        )}
        {activeTab === 'attractions' && (
          <div className="recommendations-grid">
            {attractions.map(attraction => renderItem(attraction, 'attraction'))}
          </div>
        )}
      </div>

      {selectedItem && (
        <div className="modal-overlay" onClick={() => setSelectedItem(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedItem(null)}>×</button>
            {selectedItem.type === 'hotel' && (
              <div className="modal-details">
                <h2>{(selectedItem.item as Hotel).name}</h2>
                <p><strong>Location:</strong> {(selectedItem.item as Hotel).address}</p>
                <p><strong>Amenities:</strong> {(selectedItem.item as Hotel).amenities}</p>
                <p><strong>Rating:</strong> ⭐ {(selectedItem.item as Hotel).rating}</p>
                <p><strong>Price:</strong> ${(selectedItem.item as Hotel).price_per_night} per night</p>
                <p>{(selectedItem.item as Hotel).description}</p>
                <button
                  className="book-button"
                  onClick={() => handleBook('hotel', selectedItem.item.id)}
                >
                  Book Hotel
                </button>
              </div>
            )}
            {selectedItem.type === 'flight' && (
              <div className="modal-details">
                <h2>{(selectedItem.item as Flight).airline}</h2>
                <p><strong>Route:</strong> {(selectedItem.item as Flight).origin} → {(selectedItem.item as Flight).destination}</p>
                <p><strong>Departure:</strong> {(selectedItem.item as Flight).departure_date} at {(selectedItem.item as Flight).departure_time}</p>
                <p><strong>Arrival:</strong> {(selectedItem.item as Flight).arrival_time}</p>
                <p><strong>Duration:</strong> {(selectedItem.item as Flight).duration}</p>
                <p><strong>Class:</strong> {(selectedItem.item as Flight).flight_class}</p>
                <p><strong>Stops:</strong> {(selectedItem.item as Flight).stops}</p>
                <p><strong>Price:</strong> ${(selectedItem.item as Flight).price}</p>
                <button
                  className="book-button"
                  onClick={() => handleBook('flight', selectedItem.item.id)}
                >
                  Book Flight
                </button>
              </div>
            )}
            {selectedItem.type === 'attraction' && (
              <div className="modal-details">
                <h2>{(selectedItem.item as Attraction).name}</h2>
                <p><strong>Location:</strong> {(selectedItem.item as Attraction).address}</p>
                <p><strong>Category:</strong> {(selectedItem.item as Attraction).category}</p>
                <p><strong>Opening Hours:</strong> {(selectedItem.item as Attraction).opening_hours}</p>
                <p><strong>Rating:</strong> ⭐ {(selectedItem.item as Attraction).rating}</p>
                <p><strong>Price:</strong> ${(selectedItem.item as Attraction).price === 0 ? 'Free' : (selectedItem.item as Attraction).price}</p>
                <p>{(selectedItem.item as Attraction).description}</p>
                <button
                  className="book-button"
                  onClick={() => handleBook('attraction', selectedItem.item.id)}
                >
                  Buy Ticket
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {bookingSuccess && (
        <div className="booking-success">
          {bookingSuccess}
        </div>
      )}
    </div>
  );
}

