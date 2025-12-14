import { useState } from 'react';
import LandingPage from './components/LandingPage';
import RecommendationsTabs from './components/RecommendationsTabs';
import Chatbot from './components/Chatbot';
import { api } from './api';
import type { Recommendations } from './types';
import './App.css';

function App() {
  const [recommendations, setRecommendations] = useState<Recommendations | null>(null);
  const [currentPlan, setCurrentPlan] = useState<string>('');
  const [currentDay, setCurrentDay] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [chatbotOpen, setChatbotOpen] = useState(false);

  const handlePlanSubmit = async (plan: string) => {
    setIsLoading(true);
    setCurrentPlan(plan);
    try {
      const data = await api.processTravelPlan(plan);
      setRecommendations(data);
      setCurrentDay(1);
    } catch (error) {
      console.error('Error processing travel plan:', error);
      alert('Failed to process travel plan. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChatMessage = async (message: string) => {
    try {
      const data = await api.chatWithAgent(message, currentPlan);
      setRecommendations(data);
    } catch (error) {
      console.error('Error chatting with agent:', error);
    }
  };

  const handleDayChange = async (day: number) => {
    setCurrentDay(day);
    // You can fetch day-specific recommendations here if needed
    // For now, we'll just update the day
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Planning your trip...</p>
      </div>
    );
  }

  if (!recommendations) {
    return (
      <>
        <LandingPage onPlanSubmit={handlePlanSubmit} />
        <Chatbot
          onMessage={handleChatMessage}
          isOpen={chatbotOpen}
          onToggle={() => setChatbotOpen(!chatbotOpen)}
        />
      </>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Your Travel Plan</h1>
        <button className="new-plan-button" onClick={() => setRecommendations(null)}>
          New Plan
        </button>
      </header>
      <RecommendationsTabs
        hotels={recommendations.hotels}
        flights={recommendations.flights}
        attractions={recommendations.attractions}
        days={recommendations.days}
        currentDay={currentDay}
        onDayChange={handleDayChange}
      />
      <Chatbot
        onMessage={handleChatMessage}
        isOpen={chatbotOpen}
        onToggle={() => setChatbotOpen(!chatbotOpen)}
      />
    </div>
  );
}

export default App;
