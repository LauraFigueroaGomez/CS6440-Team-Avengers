from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.patient import Patient, PatientCreate, PatientSearch
from app.repositories.patient_repository import PatientRepository
from app.utils.auth import verify_token

router = APIRouter()
repo = PatientRepository()

@router.post("/", response_model=Patient, summary="Create patient")
def create_patient(payload: PatientCreate, user=Depends(verify_token)):
    return repo.create(payload)

@router.get("/{patient_id}", response_model=Patient, summary="Get patient by id")
def get_patient(patient_id: str, user=Depends(verify_token)):
    p = repo.get(patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

@router.get("/search", response_model=List[Patient], summary="Search patients")
def search_patients(q: PatientSearch = Depends(), user=Depends(verify_token)):
    return repo.search(q)
