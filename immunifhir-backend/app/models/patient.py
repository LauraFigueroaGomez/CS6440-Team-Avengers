from typing import Optional
from pydantic import BaseModel, Field

class PatientBase(BaseModel):
    identifier: Optional[str]
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = Field(None, pattern=r"^(male|female|other|unknown)$")
    birth_date: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    immunization_count: int = 0

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: str

class PatientSearch(BaseModel):
    identifier: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[str] = None
