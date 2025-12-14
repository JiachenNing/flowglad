import { useState } from 'react';
import './LandingPage.css';

interface LandingPageProps {
  onPlanSubmit: (plan: string) => void;
}

export default function LandingPage({ onPlanSubmit }: LandingPageProps) {
  const [plan, setPlan] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (plan.trim()) {
      onPlanSubmit(plan);
    }
  };

  return (
    <div className="landing-page">
      <div className="landing-content">
        <h1 className="landing-title">AI Travel Agent</h1>
        <p className="landing-subtitle">Plan your perfect trip with AI assistance</p>
        <form onSubmit={handleSubmit} className="plan-form">
          <textarea
            className="plan-input"
            placeholder="Tell us about your travel plans...&#10;&#10;Example: I'm planning a 7-day trip to Japan, starting with three days in Tokyo exploring Shibuya, Asakusa, and Meiji Shrine, plus a day trip to Hakone for nature and an onsen. I'll then take the Shinkansen to Kyoto for two days visiting Fushimi Inari."
            value={plan}
            onChange={(e) => setPlan(e.target.value)}
            rows={8}
          />
          <button type="submit" className="submit-button">
            Plan My Trip
          </button>
        </form>
      </div>
    </div>
  );
}

