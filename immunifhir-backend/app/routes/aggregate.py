from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.models.patient import PatientSearch, PatientCreate, Patient
from app.repositories.patient_repository import PatientRepository
from app.repositories.immunization_repository import ImmunizationRepository
from app.services.state_query_service import StateQueryService
from app.services.normalization_service import NormalizationService
from app.utils.auth import verify_token

router = APIRouter()
prepo = PatientRepository()
irepo = ImmunizationRepository()
state = StateQueryService()
norm = NormalizationService()

@router.post("/run", summary="Aggregate from mock states → normalize → (optionally) persist")
async def run(search: PatientSearch, user=Depends(verify_token)) -> Dict[str, Any]:
    try:
        matches = prepo.search(search)
        patient: Patient = matches[0] if matches else prepo.create(
            PatientCreate(**search.dict(exclude_none=True))
        )

        results = await state.fetch_all(search.dict(exclude_none=True))
        items = norm.aggregate(
            NY=results.get("NY"),
            NJ=results.get("NJ"),
            PA=results.get("PA"),
        )

        for i in items:
            i.patient_id = patient.id

        saved = irepo.create_many(items) if items else []

        return {"patient": patient, "count": len(saved), "immunizations": saved}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Normalization error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Aggregate run failed: {str(e)}")
