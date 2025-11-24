# ImmuniFHIR Backend  
**CS 6440 — Introduction to Health Informatics**  
**Team Avengers**

---

## 📖 Project Overview
The **ImmuniFHIR Backend** is a FastAPI-based service designed to provide APIs for managing immunization and patient data.  
It integrates with external **FHIR servers** to exchange healthcare information and uses **Supabase** for authentication and database management.

---

## ⚙️ Tech Stack

- **Language:** Python 3.10  
- **Framework:** FastAPI  
- **Database & Auth:** Supabase (PostgreSQL)  
- **Deployment:** Render (Free Plan)  
- **CI/CD:** GitHub Actions  
- **Testing:** Pytest  

---

## 🚀 Running the App Locally
- cd immunifhir-backend 
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- export SUPABASE_URL="askteam"
- export SUPABASE_KEY="askteam"
- uvicorn app.main:app --reload
- The app will be available at http://127.0.0.1:8000


## Running the Front-End Application 
- cd immunifhir-frontend/immunifhir-frontend
- npm run dev 
