
from typing import List, Optional
from app.utils.config import supabase
from app.models.patient import Patient, PatientCreate, PatientSearch

TABLE = "patients"

class PatientRepository:
    def create(self, payload: PatientCreate) -> Patient:
        res = supabase.table(TABLE).insert(payload.dict()).execute()
        return Patient(**res.data[0])

    def get(self, patient_id: str) -> Optional[Patient]:
        res = supabase.table(TABLE).select("*").eq("id", patient_id).single().execute()
        return Patient(**res.data) if res.data else None

    def search(self, query: PatientSearch) -> List[Patient]:
        q = supabase.table(TABLE).select("*")
        if query.identifier: q = q.eq("identifier", query.identifier)
        if query.first_name: q = q.ilike("first_name", f"%{query.first_name}%")
        if query.last_name:  q = q.ilike("last_name", f"%{query.last_name}%")
        if query.birth_date: q = q.eq("birth_date", str(query.birth_date))
        res = q.execute()
        return [Patient(**row) for row in (res.data or [])]
