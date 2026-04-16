# Abhimanyu AI — AI-Powered Interview Platform

Abhimanyu is an AI-driven mock interview platform that parses your resume, generates personalized interview questions using Google Gemini, conducts a live voice interview, and delivers a detailed performance evaluation.

---

## Features

- **Resume Upload** — Drag & drop your PDF/DOCX resume. Skills are auto-extracted and matched against a comprehensive skills database
- **AI Skill & Role Suggestions** — Gemini suggests additional skills and suitable roles based on your resume
- **Custom Interview Setup** — Choose your target role, difficulty (Easy / Medium / Hard), and number of questions (10 / 20 / 25 / 30)
- **Live Voice Interview** — Conduct the interview via speech recognition. AI reads questions aloud and listens to your answers
- **Smart Retry** — If Gemini is busy, the system automatically retries up to 3 times with a 4s delay before showing a manual retry option
- **Answer Tracking** — All answers are stored in a fixed-size array matching the number of questions. Unanswered questions are marked as "Not answered"
- **AI Evaluation** — Gemini evaluates every answer and returns an overall score, feedback summary, and per-question analysis with strengths and improvements
- **Results Dashboard** — Visual breakdown of technical ability, communication, and confidence scores
- **User Auth** — Signup/login with bcrypt password hashing and MongoDB storage

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 14, Tailwind CSS |
| Backend | FastAPI, Python 3.13 |
| AI | Google Gemini 2.5 Flash (`google-genai`) |
| Database | MongoDB |
| Resume Parsing | pdfplumber |

---

## Project Structure

```
abhimanyu-ai/
├── backend/
│   ├── main.py               # FastAPI routes
│   ├── gemini_service.py     # Gemini AI calls with retry logic
│   ├── resume_parser.py      # PDF skill extraction
│   ├── emotion_detection.py  # Emotion/confidence analysis
│   ├── database.py           # MongoDB connection
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    └── app/
        ├── page.js           # Landing page
        ├── signup/           # Login & signup
        ├── upload/           # Resume upload & interview setup
        ├── interview/        # Live voice interview
        ├── dashboard/        # Results & scores
        └── components/
            ├── Navbar.js
            └── Footer.js
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB running locally or a MongoDB Atlas URI
- Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and fill in your values

# Start the server
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Environment Variables

Create a `.env` file in the `backend/` folder:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URL=mongodb://localhost:27017
```

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `MONGO_URL` | MongoDB connection string (local or Atlas) |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register a new user |
| POST | `/login` | Authenticate a user |
| POST | `/upload-resume` | Parse resume and extract skills |
| POST | `/generate-questions` | Generate interview questions via Gemini |
| POST | `/evaluate-interview` | Evaluate answers and return scores |
| POST | `/save-result` | Save interview result to MongoDB |

---

## How It Works

1. **Upload Resume** → Skills extracted from PDF using `pdfplumber`
2. **Configure** → Select role, difficulty, and number of questions
3. **Interview** → Gemini generates questions; browser Speech API handles voice I/O
4. **Evaluate** → Answers sent to Gemini for scoring with per-question feedback
5. **Results** → Dashboard shows overall score, technical ability, and communication metrics
