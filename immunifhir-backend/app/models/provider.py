from typing import Optional
from pydantic import BaseModel

class ProviderBase(BaseModel):
    name: str
    npi: Optional[str] = None
    organization: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ProviderCreate(ProviderBase):
    pass

class Provider(ProviderBase):
    id: str
