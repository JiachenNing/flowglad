# Quick Start Guide

## Prerequisites
- Python 3.8+ 
- Node.js 18+
- npm or yarn

## Quick Start (Option 1: Using the script)

```bash
./start.sh
```

This will automatically:
1. Set up the backend virtual environment
2. Install all dependencies
3. Start both servers

## Quick Start (Option 2: Manual)

### Terminal 1 - Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Open http://localhost:5173 in your browser
2. Enter your travel plan in the textbox
3. Browse recommendations in the three tabs
4. Use the floating chatbot (💬 button) to refine preferences
5. Click on items to view details and book

## Example Travel Plans

**General:**
```
I want to go to Europe
```

**Specific:**
```
I'm planning a 7-day trip to Japan, starting with three days in Tokyo exploring Shibuya, Asakusa, and Meiji Shrine, plus a day trip to Hakone for nature and an onsen. I'll then take the Shinkansen to Kyoto for two days visiting Fushimi Inari.
```

## Chatbot Examples

Try these in the chatbot:
- "I want the trip to be chill, I love nature over history"
- "I will travel with my parents"
- "Make it more budget-friendly"

