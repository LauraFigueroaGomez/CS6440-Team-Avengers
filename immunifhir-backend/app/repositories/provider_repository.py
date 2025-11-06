from typing import Optional, List
import uuid
import logging
from postgrest.exceptions import APIError
from app.utils.config import supabase
from app.models.provider import Provider, ProviderCreate

logger = logging.getLogger(__name__)
TABLE = "providers"

class ProviderRepository:
    def create(self, payload: ProviderCreate) -> Provider:
        res = supabase.table(TABLE).insert(payload.dict()).execute()
        return Provider(**res.data[0])

    def get(self, provider_id: str) -> Optional[Provider]:
        logger.debug("get provider called with id=%s", provider_id)

        # validate UUID early
        try:
            uuid.UUID(provider_id)
        except (ValueError, TypeError):
            logger.debug("invalid uuid provided: %s", provider_id)
            return None

        try:
            res = supabase.table(TABLE).select("*").eq("id", provider_id).single().execute()
        except APIError as e:
            logger.exception("PostgREST APIError while fetching provider id=%s", provider_id)
            return None

        # log full response for debugging
        logger.debug("supabase response error=%s data=%s", getattr(res, "error", None), getattr(res, "data", None))

        if not res.data:
            logger.debug("no provider found for id=%s", provider_id)
            return None

        return Provider(**res.data)

    def list(self) -> List[Provider]:
        res = supabase.table(TABLE).select("*").execute()
        return [Provider(**row) for row in (res.data or [])]
