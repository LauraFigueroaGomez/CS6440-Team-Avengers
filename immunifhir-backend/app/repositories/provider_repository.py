from typing import Optional, List
from app.utils.config import supabase
from app.models.provider import Provider, ProviderCreate

TABLE = "providers"

class ProviderRepository:
    def create(self, payload: ProviderCreate) -> Provider:
        res = supabase.table(TABLE).insert(payload.dict()).execute()
        return Provider(**res.data[0])

    def get(self, provider_id: str) -> Optional[Provider]:
        res = supabase.table(TABLE).select("*").eq("id", provider_id).single().execute()
        return Provider(**res.data) if res.data else None

    def list(self) -> List[Provider]:
        res = supabase.table(TABLE).select("*").execute()
        return [Provider(**row) for row in (res.data or [])]
