from typing import List, Optional
from app.utils.config import supabase
from app.models.patient import Patient, PatientCreate, PatientSearch

TABLE = "patients"
SEARCH_VIEW = "patient_search_with_counts"

class PatientRepository:
    def create(self, payload: PatientCreate) -> Patient:
        res = supabase.table(TABLE).insert(payload.dict()).execute()
        return Patient(**res.data[0])

    def get(self, id: str) -> Optional[Patient]:
        res = supabase.table(TABLE).select("*").eq("id", id).execute()
        print(f"Database response: {res.data}")
        if res.data and len(res.data) > 0:
            return Patient(**res.data[0])
        return None

    def search(self, query: PatientSearch) -> List[Patient]:
        q = supabase.table(SEARCH_VIEW).select("*")

        if hasattr(query, "identifier") and query.identifier:
            q = q.eq("identifier", query.identifier)
        if query.first_name:
            q = q.ilike("first_name", f"%{query.first_name}%")
        if query.last_name:
            q = q.ilike("last_name", f"%{query.last_name}%")
        if query.birth_date:
            q = q.eq("birth_date", str(query.birth_date))
        res = q.execute()
        return [Patient(**row) for row in (res.data or [])]
