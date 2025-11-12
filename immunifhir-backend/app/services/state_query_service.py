from __future__ import annotations
from typing import Dict, Any
import os, httpx

class StateQueryService:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or os.getenv("BACKEND_BASE_URL") or "http://localhost:8000").rstrip("/")

    async def _smart_body(self, resp: httpx.Response):
        resp.raise_for_status()
        ct = resp.headers.get("content-type", "").lower()
        if "json" in ct:
            return resp.json()
        return resp.text

    async def fetch_all(self, patient_search: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10) as client:
            ny = await client.get(f"{self.base_url}/mock/ny", params=patient_search)
            nj = await client.get(f"{self.base_url}/mock/nj", params=patient_search)
            pa = await client.get(f"{self.base_url}/mock/pa", params=patient_search)

        return {
            "NY": await self._smart_body(ny),
            "NJ": await self._smart_body(nj),
            "PA": await self._smart_body(pa),
        }
