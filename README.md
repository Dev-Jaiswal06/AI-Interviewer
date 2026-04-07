# AI-Based Mock Technical and HR Interview System

A full-stack web application that simulates real placement interviews and provides coding practice.

## Project Structure

```
AI-Interview-System/
├── backend/                 # Flask Backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic (NLP, AI)
│   │   └── utils/          # Helper functions
│   ├── requirements.txt    # Python dependencies
│   └── seed_data.py       # Database seeding
│
└── frontend/               # React Frontend
    ├── src/
    │   ├── components/     # Reusable components
    │   ├── pages/          # Page components
    │   ├── services/      # API services
    │   └── context/        # React context
    └── package.json
```

## Features

- **Authentication**: Login, Signup, Password Reset
- **Interview Module**: Technical & HR questions with voice input
- **Resume Processing**: PDF parsing with skill extraction
- **Coding Module**: Practice problems with code execution
- **AI Evaluation**: TF-IDF & Cosine Similarity for answer grading
- **Performance Dashboard**: Detailed analytics and recommendations

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

---

## Setup Instructions (Step by Step)

### Step 1: Backend Setup

**1. Open Terminal and navigate to backend folder:**
```bash
cd C:/Users/DELL/Desktop/AI-Interview-System/backend
```

**2. Create virtual environment:**
```bash
python -m venv venv
```

**3. Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**4. Install dependencies:**
```bash
pip install -r requirements.txt
```

**5. Run database seeding (this creates sample problems):**
```bash
python seed_data.py
```

**6. Start the backend server:**
```bash
python app.py
```

Backend will run at: `http://localhost:5000`

You should see:
```
* Running on http://127.0.0.1:5000
* Restarting with reloader
```

---

### Step 2: Frontend Setup

**1. Open a NEW Terminal window and navigate to frontend:**
```bash
cd C:/Users/DELL/Desktop/AI-Interview-System/frontend
```

**2. Install dependencies:**
```bash
npm install
```

**3. Start the frontend:**
```bash
npm run dev
```

Frontend will run at: `http://localhost:3000`

---

### Step 3: Running the Application

1. Open your browser: `http://localhost:3000`
2. Register a new account
3. Login with your credentials
4. Start taking interviews!

---

## How to Use

### Taking an Interview:
1. Click "Start Mock Interview"
2. Choose interview type (Technical, HR, or Mixed)
3. Optionally upload resume for skill-based questions
4. Answer questions (use voice input or type)
5. Submit and view detailed feedback

### Practice Coding:
1. Click "Coding" in navbar
2. Select a problem
3. Choose language (Python, JavaScript, Java, C++)
4. Write your solution
5. Test and submit
6. View score and test case results

### View Dashboard:
- Track overall progress
- See strengths and weak areas
- Get personalized recommendations

---

## Tech Stack Used

| Component | Technology | Free? |
|-----------|-----------|-------|
| Frontend | React.js | Yes |
| Backend | Flask | Yes |
| Database | SQLite | Yes |
| NLP | TF-IDF + Cosine Similarity | Yes |
| Resume | PyPDF2 | Yes |
| Voice | Web Speech API | Yes |
| Coding | Judge0 (simulated) | Yes |

**All technologies used are FREE!**

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile

### Interview
- `POST /api/interview/start` - Start new interview
- `POST /api/interview/submit-answer` - Submit answer
- `POST /api/interview/complete` - Complete interview
- `GET /api/interview/history` - Get interview history

### Coding
- `GET /api/coding/problems` - Get all problems
- `GET /api/coding/problems/:id` - Get problem details
- `POST /api/coding/submit` - Submit code solution

### Evaluation
- `POST /api/evaluation/answer` - Evaluate single answer
- `POST /api/evaluation/interview/:id` - Evaluate full interview
- `GET /api/evaluation/analysis/:id` - Get analysis

### Dashboard
- `GET /api/dashboard/overview` - Get overview stats
- `GET /api/dashboard/strengths` - Get strengths
- `GET /api/dashboard/weaknesses` - Get weaknesses
- `GET /api/dashboard/recommendations` - Get recommendations

---

## Troubleshooting

### Backend Issues:
```bash
# If port 5000 is busy, change port in app/__init__.py
app.run(debug=True, port=5001)

# Update frontend API URL in src/services/api.js
const API_URL = 'http://localhost:5001/api';
```

### Frontend Issues:
```bash
# Clear cache and reinstall
rm -rf node_modules
npm install

# If CORS error, ensure backend is running
```

### Database Issues:
```bash
# Delete database and reseed
del interview_system.db
python seed_data.py
```

---

## Development

To add more features:

1. **Add more questions**: Edit `app/services/question_generator.py`
2. **Add coding problems**: Edit `seed_data.py`
3. **Customize NLP**: Edit `app/services/answer_evaluator.py`

---

## License

MIT License - Feel free to use and modify!

---

## Support

If you face any issues, check:
1. Backend terminal for errors
2. Browser console for frontend errors
3. Ensure both servers are running
