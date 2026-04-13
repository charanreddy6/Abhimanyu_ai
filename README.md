# Abhimanyu AI — AI-Powered Interview Platform

Abhimanyu is an AI-driven mock interview platform that analyzes your resume, generates personalized interview questions, and evaluates your answers with detailed feedback.

## Features

- **Resume Upload** — Parses your resume to extract skills automatically
- **Dynamic Question Generation** — AI generates tailored technical and behavioral questions based on your skills, target role, and difficulty level
- **Voice Interview** — Conduct interviews via voice with real-time confidence and emotion analysis
- **Instant Evaluation** — Get an overall score, strengths, and improvement areas powered by Gemini AI
- **User Auth** — Signup/login with secure password hashing

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 14, Tailwind CSS |
| Backend | FastAPI, Python |
| AI | Google Gemini API |
| Database | MongoDB |

## Project Structure

```
abhimanyu-ai/
├── backend/          # FastAPI server
│   ├── main.py
│   ├── gemini_service.py
│   ├── resume_parser.py
│   ├── emotion_detection.py
│   ├── database.py
│   └── .env.example
└── frontend/         # Next.js app
    └── app/
        ├── page.js
        ├── dashboard/
        ├── interview/
        ├── upload/
        └── signup/
```

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Copy and fill in your API key
cp .env.example .env

uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file in the `backend/` folder based on `.env.example`:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
