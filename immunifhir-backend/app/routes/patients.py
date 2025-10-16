# app/routes/patients.py
from fastapi import APIRouter, Depends
from app.utils.auth import verify_token

router = APIRouter()

@router.get("/", summary="Get list of patients")
def get_patients(user=Depends(verify_token)):
    return {"message": "Patients route working!", "user": user["email"]}
