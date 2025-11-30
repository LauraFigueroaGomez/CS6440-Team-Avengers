# ImmuniFHIR Backend  
**CS 6440 — Introduction to Health Informatics**  
**Team Avengers**

---

## 📖 Project Overview
ImmuniFHIR is a multi-state immunization aggregation platform developed for CS 6440 (Team Avengers).
The system retrieves immunization data from mock state registries (NY, NJ, PA), parses HL7 v2.x messages, normalizes them, persists data in Supabase, and presents the results through a secure Vue.js frontend.

This README includes:
- ✅ Backend documentation
- ✅ Frontend documentation
- ✅ Architecture diagram
- ✅ Mockups
- ✅ Test data location
- ✅ Setup & deployment instructions

---

## ⚙️ Tech Stack

- **Language:** Python 3.10  
- **Framework Backend:** FastAPI
- **Framework Frontend:** Vue 3, Vie  
- **Database & Auth:** Supabase (PostgreSQL)  
- **Deployment:** Render (Free Plan)
- **CI/CD:** GitHub Actions  
- **Testing:** Pytest

---

## Test Data
📍 Location:
 CS6440-Team-Avengers/immunifhir-backend/schema

Includes:
- HL7 sample VXU messages (NY, NJ, PA)
- Test patients

Used for:

- HL7 → JSON → FHIR testing
- Unit tests
- Aggregation validation

---

## 🚀 Running the Backend App Locally
- cd immunifhir-backend 
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- export SUPABASE_URL="askteam"
- export SUPABASE_KEY="askteam"
- export BYPASS_AUTH=true
- export SUPABASE_JWT_AUD=authenticated
- export JWT_SECRET=your_supabase_jwt_secret
- uvicorn app.main:app --reload
- The app will be available at http://127.0.0.1:8000


## 🚀 Running the Front-End Application Locally
- cd immunifhir-frontend/immunifhir-frontend
- npm install
- export VITE_BACKEND_URL=http://127.0.0.1:8000
- export VITE_SUPABASE_URL=your_url
- export VITE_SUPABASE_ANON_KEY=your_key
- npm run dev
- The app will be available at http://127.0.0.1:5173
