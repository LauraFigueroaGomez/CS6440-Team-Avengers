from typing import List
from fastapi import APIRouter, Depends
from app.models.immunization import Immunization, ImmunizationCreate
from app.repositories.immunization_repository import ImmunizationRepository
from app.utils.auth import verify_token

router = APIRouter()
repo = ImmunizationRepository()

@router.get("/by-patient/{patient_id}", response_model=List[Immunization], summary="List immunizations by patient")
def by_patient(patient_id: str, user=Depends(verify_token)):
    return repo.by_patient(patient_id)

@router.post("/bulk", response_model=List[Immunization], summary="Insert multiple immunizations")
def create_bulk(items: List[ImmunizationCreate], user=Depends(verify_token)):
    return repo.create_many(items)
