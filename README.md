# AI Credit Intelligence

AI Credit Intelligence is an end-to-end credit risk prediction system that uses machine learning to predict the likelihood of loan default.

The project uses **XGBoost and Random Forest** for credit-risk classification, with threshold tuning, model evaluation, explainability, and an interactive web application.

## Project Structure

```text
AI-Credit-Intelligence/
├── frontend/
├── backend/
├── ml-service/
├── README.md
└── ...

Requirements
Python 3.x
PostgreSQL
Node.js
npm

Python dependencies are listed in requirements.txt.

Install them using:
pip install -r requirements.txt

Frontend dependencies are listed in package.json.
npm install

Environment Variables
Backend .env
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
Frontend .env
VITE_API_URL=http://localhost:8000
How to Run
1. Start PostgreSQL

Make sure PostgreSQL is running and the required database has been created.

2. Run Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

3. Run Frontend

Open another terminal:
cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

Main Files
Backend

backend/app/main.py

Main FastAPI application and backend entry point.

Machine Learning

ml-service/src/

Contains the machine learning training, evaluation, prediction, and model-related files.

Frontend

frontend/

Contains the React frontend application.

Deployment
Frontend: Vercel
Backend: Render
Database: PostgreSQL

For production deployment, update the frontend environment variable:

VITE_API_URL=https://ai-credit-intelligence.onrender.com
