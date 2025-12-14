# AI Travel Agent

A full-stack AI-powered travel planning application with a React/TypeScript frontend and FastAPI backend.

## Features

- **Intelligent Travel Planning**: Input your travel plans (general or specific) and get personalized recommendations
- **Three Recommendation Categories**: Hotels, Flights, and Tourist Attractions
- **Multi-day Trip Support**: Navigate through different days of your trip
- **AI Chatbot**: Refine your trip preferences in real-time through a floating chatbot
- **Booking System**: Book hotels, flights, and purchase attraction tickets directly from the interface

## Project Structure

```
flowglad/
├── backend/          # FastAPI backend
│   ├── main.py      # API endpoints
│   ├── database.py  # SQLite database setup and models
│   ├── models.py    # Pydantic models
│   └── requirements.txt
├── frontend/        # React/TypeScript frontend
│   └── src/
│       ├── components/
│       │   ├── LandingPage.tsx
│       │   ├── RecommendationsTabs.tsx
│       │   └── Chatbot.tsx
│       ├── App.tsx
│       ├── api.ts
│       └── types.ts
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (or the port shown in the terminal)

## Usage

1. **Start the backend server** (port 8000)
2. **Start the frontend server** (port 5173)
3. **Open your browser** and navigate to the frontend URL
4. **Enter your travel plan** in the textbox on the landing page
   - General: "I want to go to Europe"
   - Specific: "I'm planning a 7-day trip to Japan, starting with three days in Tokyo..."
5. **Browse recommendations** in the three tabs (Hotels, Flights, Attractions)
6. **Use the chatbot** (floating button on the right) to refine your preferences
7. **Navigate between days** if your trip spans multiple days
8. **Click on items** to view details and book

## Database

The SQLite database (`travel_agent.db`) is automatically created when you first run the backend. It includes sample data for:
- Hotels in various cities (Tokyo, Kyoto, Hakone, Paris, Rome, Barcelona)
- Flights between major cities
- Tourist attractions with categories (nature, history, culture)

## API Endpoints

- `POST /api/travel-plan` - Process travel plan and get recommendations
- `POST /api/chat` - Chat with AI agent to refine recommendations
- `GET /api/recommendations/day/{day}` - Get recommendations for a specific day
- `POST /api/book` - Book hotels, flights, or attraction tickets

## Technologies Used

- **Frontend**: React 19, TypeScript, Vite
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Styling**: CSS3 with modern gradients and animations

