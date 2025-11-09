from typing import Dict, Any

class FHIRService:
    def patient(self, p: dict) -> Dict[str, Any]:
        return {
            "resourceType": "Patient",
            "name": [{"family": p.get("last_name"), "given": [p.get("first_name")]}],
            "birthDate": str(p.get("birth_date")) if p.get("birth_date") else None,
            "gender": p.get("gender") or "unknown"
        }

    def immunization(self, im: dict, patient_ref: str) -> Dict[str, Any]:
        return {
            "resourceType": "Immunization",
            "status": im.get("status", "completed"),
            "vaccineCode": {
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/cvx",
                    "code": im.get("vaccine_code"),
                    "display": im.get("vaccine_name"),
                }]
            },
            "patient": {"reference": patient_ref},
            "occurrenceDateTime": str(im.get("date_administered")) if im.get("date_administered") else None
        }