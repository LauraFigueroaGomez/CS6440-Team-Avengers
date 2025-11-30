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

---

## Front-end Dcoumentation 
Front-End Stack: Vue.js, Pinia, Vite

Features

- Multi-State Search: Query immunization records across NY, NJ, and PA simultaneously
- Live Aggregation: Real-time data fetching from state registries (not cached)
- Patient Management: Search patients by name and date of birth
- Immunization History: View complete vaccination records with sorting and filtering
- State Summary: See record counts per state registry
- Secure Authentication: JWT-based auth with Supabase

## Run the Front-End Application Locally
- cd immunifhir-frontend/immunifhir-frontend
- npm install
- export VITE_BACKEND_URL=http://127.0.0.1:8000
- export VITE_SUPABASE_URL=your_url
- export VITE_SUPABASE_ANON_KEY=your_key
- npm run dev
- The app will be available at http://127.0.0.1:5173 or your respective localhost.

## Test Data and Login Credentials

 Email: test@example.com
 Password: test123

 Sample Patient Records (Available in all 3 states)

 1. John Smith
   - DOB: 1985-03-15
   - MRN: PAT001
   - Has 12 immunization records
 2. Sarah Johnson
   - DOB: 1990-07-22
   - MRN: PAT002
   - Has 10 immunization records
 3. Michael Brown
   - DOB: 1978-11-08
   - MRN: PAT003
   - Has 15 immunization records

## Production URLs
Frontend: https://cs6440-team-avengers-1-frontend.onrender.com
Backend: https://cs6440-team-avengers-1-backend.onrender.com



