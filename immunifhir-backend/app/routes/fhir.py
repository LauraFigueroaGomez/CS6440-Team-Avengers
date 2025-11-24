from fastapi import APIRouter, HTTPException
from app.repositories.patient_repository import PatientRepository
from app.repositories.immunization_repository import ImmunizationRepository
from app.services.fhir_service import FHIRService

router = APIRouter()

patient_repo = PatientRepository()
immunization_repo = ImmunizationRepository()
fhir_service = FHIRService()


@router.get("/patient/{patient_id}", summary="Get FHIR Patient by ID")
async def get_fhir_patient(patient_id: str):
    patient = patient_repo.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return fhir_service.patient(patient.dict())


@router.get("/immunization/{immunization_id}", summary="Get FHIR Immunization by ID")
async def get_fhir_immunization(immunization_id: str):
    immunization = immunization_repo.get(immunization_id)
    if not immunization:
        raise HTTPException(status_code=404, detail="Immunization not found")

    im_dict = immunization.dict()
    patient_id = im_dict.get("patient_id")
    if not patient_id:
        raise HTTPException(status_code=400, detail="Immunization record missing patient_id")

    patient_ref = f"Patient/{patient_id}"

    return fhir_service.immunization(im_dict, patient_ref)
