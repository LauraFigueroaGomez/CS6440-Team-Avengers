from typing import List, Optional
from app.utils.config import supabase
from app.models.immunization import Immunization, ImmunizationCreate
from fastapi.encoders import jsonable_encoder


TABLE = "immunizationrecords"

class ImmunizationRepository:
    def create_many(self, items: List[ImmunizationCreate]) -> List[Immunization]:
        rows = [jsonable_encoder(i, exclude_none=True) for i in items]
        res = supabase.table(TABLE).insert(rows).execute()
        return [Immunization(**row) for row in (res.data or [])]

    def by_patient(self, patient_id: str) -> List[Immunization]:
        res = supabase.table(TABLE).select("*").eq("patient_id", patient_id).execute()
        return [Immunization(**row) for row in (res.data or [])]

    def get(self, immunization_id: str) -> Optional[Immunization]:
        """Fetch a single immunization record by its ID."""
        res = supabase.table(TABLE).select("*").eq("id", immunization_id).execute()
        if res.data and len(res.data) > 0:
            return Immunization(**res.data[0])
        return None
