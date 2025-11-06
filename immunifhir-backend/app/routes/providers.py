from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.provider import Provider, ProviderCreate
from app.repositories.provider_repository import ProviderRepository
from app.utils.auth import verify_token

router = APIRouter()
repo = ProviderRepository()

@router.post("/", response_model=Provider, summary="Create provider")
def create_provider(payload: ProviderCreate, user=Depends(verify_token)):
    return repo.create(payload)

@router.get("/{provider_id}", response_model=Provider, summary="Get provider by id")
def get_provider(provider_id: str, user=Depends(verify_token)):
    p = repo.get(provider_id)
    if not p:
        raise HTTPException(status_code=404, detail="Provider not found")
    return p

@router.get("/", response_model=List[Provider], summary="List providers")
def list_providers(user=Depends(verify_token)):
    return repo.list()
