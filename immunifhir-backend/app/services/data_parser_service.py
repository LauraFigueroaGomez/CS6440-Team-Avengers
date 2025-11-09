from typing import Dict, Any, Union
from hl7apy import parser
from xmltodict import parse as xml_parse
from datetime import date
import json
import re
from datetime import datetime
from app.models.immunization import ImmunizationCreate
from app.models.patient import PatientCreate
from app.models.provider import ProviderCreate

class DataParserService:
    @staticmethod
    def parse_hl7(hl7_message: str) -> Dict[str, Any]:
        """
        Parse HL7 message and convert it to a dictionary format
        """
        try:
            if not hl7_message or not isinstance(hl7_message, str):
                raise ValueError("Invalid HL7 message format")

            # Split message into segments and parse manually
            segments = [s for s in re.split(r'[\r\n]+', hl7_message.strip()) if s]
            if not segments or not any(seg.startswith('MSH|') for seg in segments):
                raise ValueError("Invalid HL7 message: Missing MSH segment")

            result = {"patient": {}, "immunization": {}}
            has_pid = False
            has_rxa = False

            for segment in segments:
                fields = segment.split('|')

                if segment.startswith('PID|'):
                    has_pid = True

                    id_val = fields[3].split('^')[0] if len(fields) > 3 and fields[3] else None
                    name_val = fields[5] if len(fields) > 5 else ""
                    name_components = name_val.split('^') if name_val else []
                    last_name = name_components[0] if len(name_components) > 0 else None
                    first_name = name_components[1] if len(name_components) > 1 else None
                    birth_date = fields[7] if len(fields) > 7 else None
                    gender = fields[8].lower() if len(fields) > 8 and fields[8] else None

                    result["patient"].update({
                        "identifier": id_val,
                        "last_name": last_name,
                        "first_name": first_name,
                        "birth_date": birth_date,
                        "gender": gender,
                    })

                elif segment.startswith('RXA|'):
                    has_rxa = True
                    # HL7 RXA-3 date, RXA-5 code^text, RXA-15 lot (often 15 but your comment said 9—varies)
                    date_admin = fields[3] if len(fields) > 3 else None
                    vacc = fields[5] if len(fields) > 5 else ""
                    vacc_components = vacc.split('^') if vacc else []
                    vaccine_code = vacc_components[0] if len(vacc_components) > 0 else None
                    vaccine_name = vacc_components[1] if len(vacc_components) > 1 else None

                    lot_number = None
                    for idx in (9, 15):
                        if len(fields) > idx and fields[idx]:
                            lot_number = fields[idx]
                            break

                    result["immunization"].update({
                        "vaccine_code": vaccine_code,
                        "vaccine_name": vaccine_name,
                        "date_administered": date_admin,
                        "lot_number": lot_number
                    })

            if not has_pid:
                raise ValueError("Missing PID segment")

            if not has_rxa:
                result.setdefault("immunization", {})

            return result

        except Exception as e:
            raise ValueError(f"Error parsing HL7 message: {str(e)}")

    @staticmethod
    def parse_xml(xml_data: str) -> Dict[str, Any]:
        """
        Parse XML/SOAP response and convert it to a dictionary format
        """
        data = xml_parse(xml_data)

        if "Immunization" in data and isinstance(data["Immunization"], dict):
            rec = data["Immunization"]
            return {
                "patient": {"identifier": rec.get("PatientId")},
                "immunization": {
                    "vaccine_code": rec.get("VaccineCode"),
                    "vaccine_name": rec.get("Vaccine"),
                    "status": "completed",
                    "date_administered": rec.get("Date"),
                    "lot_number": rec.get("LotNumber"),
                },
            }

        root = next(iter(data.values())) if isinstance(data, dict) else {}
        if isinstance(root, dict):
            return {
                "patient": {"identifier": root.get("PatientId") or root.get("PatientID")},
                "immunization": {
                    "vaccine_code": root.get("VaccineCode"),
                    "vaccine_name": root.get("Vaccine") or root.get("VaccineName"),
                    "status": "completed",
                    "date_administered": root.get("Date") or root.get("DateAdministered"),
                    "lot_number": root.get("LotNumber"),
                },
            }
        return {"patient": {}, "immunization": {}}

    @staticmethod
    def parse_rest_json(json_data: Union[str, Dict]) -> Dict[str, Any]:
        """
        Parse REST JSON response and convert it to a dictionary format
        """
        data = json.loads(json_data) if isinstance(json_data, str) else dict(json_data)

        if isinstance(data.get("data"), dict):
            data = data["data"]

        pid  = data.get("patientId") or data.get("patient_id") or data.get("patientID")
        vacc = data.get("vaccineName") or data.get("vaccine")
        code = data.get("vaccineCode") or data.get("cvx") or data.get("CVX")
        date_admin = (data.get("administrationDate") or data.get("date")
                      or data.get("DateAdministered"))

        return {
            "patient": {
                "identifier": pid,
                "first_name": data.get("firstName"),
                "last_name": data.get("lastName"),
                "birth_date": data.get("birthDate") or data.get("dob"),
                "gender": (data.get("gender") or "").lower(),
                "address": data.get("address"),
                "phone": data.get("phone"),
                "email": data.get("email"),
            },
            "immunization": {
                "vaccine_code": code,
                "vaccine_name": vacc,
                "status": data.get("status", "completed"),
                "date_administered": date_admin,
                "lot_number": data.get("lotNumber"),
                "site": data.get("site"),
                "route": data.get("route"),
                "dose_quantity": data.get("doseQuantity"),
                "notes": data.get("notes"),
            },
        }

    @staticmethod
    def to_patient_create(data: Dict[str, Any]) -> PatientCreate:
        """
        Convert parsed data to PatientCreate model
        """
        patient_data = data.get("patient", {})
        return PatientCreate(
            identifier=patient_data.get("identifier"),
            first_name=patient_data.get("first_name"),
            last_name=patient_data.get("last_name"),
            birth_date=DataParserService._parse_date(patient_data.get("birth_date")),
            gender=patient_data.get("gender"),
            address=patient_data.get("address"),
            phone=patient_data.get("phone"),
            email=patient_data.get("email")
        )

    @staticmethod
    def to_provider_create(data: Dict[str, Any]) -> ProviderCreate:
        """
        Convert parsed data to ProviderCreate model
        """
        provider_data = data.get("provider", {})
        return ProviderCreate(
            name=provider_data.get("name"),
            npi=provider_data.get("npi"),
            organization=provider_data.get("organization"),
            address=provider_data.get("address"),
            phone=provider_data.get("phone")
        )

    @staticmethod
    def to_immunization_create(data: Dict[str, Any]) -> ImmunizationCreate:
        """
        Convert parsed data to ImmunizationCreate model
        """
        imm_data = data.get("immunization", {})
        return ImmunizationCreate(
            vaccine_code=imm_data.get("vaccine_code"),
            vaccine_name=imm_data.get("vaccine_name"),
            status=imm_data.get("status", "completed"),
            date_administered=DataParserService._parse_date(imm_data.get("date_administered")),
            lot_number=imm_data.get("lot_number"),
            site=imm_data.get("site"),
            route=imm_data.get("route"),
            dose_quantity=imm_data.get("dose_quantity"),
            notes=imm_data.get("notes")
        )

    @staticmethod
    def _parse_date(v: Union[str, None]) -> Union[date, None]:
        if not v or not isinstance(v, str): return None
        v = v.strip()
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%Y%m", "%Y",
                    "%Y%m%d%H%M%S", "%Y%m%d%H%M"):
            try:
                return datetime.strptime(v, fmt).date()
            except:
                pass
        return None