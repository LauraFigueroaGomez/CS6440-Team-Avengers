from typing import Optional
from pydantic import BaseModel, Field

class PatientBase(BaseModel):
    identifier: Optional[str] = None
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    gender: Optional[str] = Field(None, pattern="^(male|female|other|unknown)$")
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: str

class PatientSearch(BaseModel):
    identifier: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[str] = None
