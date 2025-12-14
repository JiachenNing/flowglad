import type { Recommendations, BookingResponse } from './types';

const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async processTravelPlan(plan: string, preferences?: string): Promise<Recommendations> {
    const response = await fetch(`${API_BASE_URL}/api/travel-plan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ plan, preferences }),
    });
    if (!response.ok) {
      throw new Error('Failed to process travel plan');
    }
    return response.json();
  },

  async chatWithAgent(message: string, currentPlan?: string): Promise<Recommendations> {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, current_plan: currentPlan }),
    });
    if (!response.ok) {
      throw new Error('Failed to chat with agent');
    }
    return response.json();
  },

  async getRecommendationsForDay(day: number, locations?: string): Promise<Recommendations> {
    const url = new URL(`${API_BASE_URL}/api/recommendations/day/${day}`);
    if (locations) {
      url.searchParams.append('locations', locations);
    }
    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error('Failed to get recommendations');
    }
    return response.json();
  },

  async bookItem(type: 'hotel' | 'flight' | 'attraction', id: number, date?: string): Promise<BookingResponse> {
    const response = await fetch(`${API_BASE_URL}/api/book`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ type, id, date }),
    });
    if (!response.ok) {
      throw new Error('Failed to book item');
    }
    return response.json();
  },
};

