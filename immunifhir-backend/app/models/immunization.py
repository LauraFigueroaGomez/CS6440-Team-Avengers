from typing import Optional
from datetime import date
from pydantic import BaseModel

class ImmunizationBase(BaseModel):
    patient_id: Optional[str] = None
    provider_id: Optional[str] = None
    vaccine_code: Optional[str] = None
    vaccine_name: Optional[str] = None
    status: Optional[str] = "completed"
    date_administered: Optional[date] = None
    lot_number: Optional[str] = None
    expiration_date: Optional[date] = None
    site: Optional[str] = None
    route: Optional[str] = None
    dose_quantity: Optional[str] = None
    notes: Optional[str] = None
    source_state: Optional[str] = None

class ImmunizationCreate(ImmunizationBase):
    pass

class Immunization(ImmunizationBase):
    id: str
