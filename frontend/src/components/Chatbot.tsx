import { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

interface ChatbotProps {
  onMessage: (message: string) => void;
  isOpen: boolean;
  onToggle: () => void;
}

export default function Chatbot({ onMessage, isOpen, onToggle }: ChatbotProps) {
  const [messages, setMessages] = useState<Array<{ text: string; sender: 'user' | 'bot' }>>([
    { text: "Hi! I'm your AI travel assistant. How can I help refine your trip?", sender: 'bot' }
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: 'user' as const };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    // Send to parent component
    onMessage(input);

    // Bot response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        text: "Got it! I've updated your recommendations based on your preferences.",
        sender: 'bot'
      }]);
    }, 500);
  };

  return (
    <>
      <button className="chatbot-toggle" onClick={onToggle}>
        💬
      </button>
      {isOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <h3>Travel Assistant</h3>
            <button onClick={onToggle}>×</button>
          </div>
          <div className="chatbot-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="chatbot-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type your message..."
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </>
  );
}

