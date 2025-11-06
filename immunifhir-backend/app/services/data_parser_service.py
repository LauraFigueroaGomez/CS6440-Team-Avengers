from typing import Dict, Any, Union
from hl7apy import parser
from xmltodict import parse as xml_parse
import json
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
            segments = hl7_message.strip().split('\n')
            if not segments or not any(seg.startswith('MSH|') for seg in segments):
                raise ValueError("Invalid HL7 message: Missing MSH segment")

            result = {
                "patient": {},
                "immunization": {}
            }
            
            has_pid = False
            for segment in segments:
                fields = segment.split('|')
                
                if segment.startswith('PID|'):
                    has_pid = True
                    if len(fields) < 9:  # Minimum fields required for our parsing
                        raise ValueError("Invalid PID segment structure")
                    
                    # Parse PID segment
                    name_components = fields[5].split('^') if len(fields) > 5 else []
                    if len(name_components) < 2:
                        raise ValueError("Invalid patient name format in PID segment")
                    
                    result["patient"].update({
                        "identifier": fields[3].split('^')[0] if len(fields) > 3 else None,
                        "last_name": name_components[0],
                        "first_name": name_components[1],
                        "birth_date": fields[7],
                        "gender": fields[8].lower(),
                    })
                
                elif segment.startswith('RXA|'):
                    if len(fields) < 6:  # Minimum fields required for our parsing
                        raise ValueError("Invalid RXA segment structure")
                    
                    # Parse RXA segment
                    vaccine_components = fields[5].split('^')
                    if len(vaccine_components) < 2:
                        raise ValueError("Invalid vaccine format in RXA segment")
                    
                    result["immunization"].update({
                        "vaccine_code": vaccine_components[0],
                        "vaccine_name": vaccine_components[1],
                        "date_administered": fields[3],
                        "lot_number": fields[9] if len(fields) > 9 else None  # Lot Number is actually in field 9
                    })
            
            if not has_pid:
                raise ValueError("Missing PID segment")
                
            return result
        except Exception as e:
            raise ValueError(f"Error parsing HL7 message: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing HL7 message: {str(e)}")

    @staticmethod
    def parse_xml(xml_data: str) -> Dict[str, Any]:
        """
        Parse XML/SOAP response and convert it to a dictionary format
        """
        try:
            # Parse XML to dict
            data = xml_parse(xml_data)
            
            # Extract data based on your XML structure
            # This is an example based on your NJPatientrecords.xml structure
            if "NJMockData" in data:
                record = data["NJMockData"]
                result = {
                    "patient": {
                        "identifier": record["Patient"]["PatientID"],
                        "first_name": record["Patient"]["FirstName"],
                        "last_name": record["Patient"]["LastName"],
                        "birth_date": record["Patient"]["DOB"],
                        "gender": record["Patient"]["Gender"].lower(),
                        "address": record["Patient"]["Address"],
                        "phone": record["Patient"]["Phone"],
                        "email": record["Patient"]["Email"]
                    },
                    "provider": {
                        "name": record["Provider"]["n"],
                        "npi": record["Provider"]["NPI"],
                        "organization": record["Provider"]["Organization"],
                        "address": record["Provider"]["Address"],
                        "phone": record["Provider"]["Phone"]
                    },
                    "immunization": {
                        "vaccine_code": record["ImmunizationRecord"]["VaccineCode"],
                        "vaccine_name": record["ImmunizationRecord"]["VaccineName"],
                        "status": record["ImmunizationRecord"]["Status"],
                        "date_administered": record["ImmunizationRecord"]["DateAdministered"],
                        "lot_number": record["ImmunizationRecord"]["LotNumber"],
                        "site": record["ImmunizationRecord"]["Site"],
                        "route": record["ImmunizationRecord"]["Route"],
                        "dose_quantity": record["ImmunizationRecord"]["DoseQuantity"],
                        "notes": record["ImmunizationRecord"]["Notes"]
                    }
                }
                return result
            raise ValueError("Invalid XML structure")
        except Exception as e:
            raise ValueError(f"Error parsing XML data: {str(e)}")

    @staticmethod
    def parse_rest_json(json_data: Union[str, Dict]) -> Dict[str, Any]:
        """
        Parse REST JSON response and convert it to a dictionary format
        """
        try:
            # Parse JSON if it's a string
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            
            # Map the JSON structure to our internal format
            # This is an example - modify based on your REST API response structure
            result = {
                "patient": {
                    "identifier": data.get("patientId"),
                    "first_name": data.get("firstName"),
                    "last_name": data.get("lastName"),
                    "birth_date": data.get("birthDate"),
                    "gender": data.get("gender", "").lower(),
                    "address": data.get("address"),
                    "phone": data.get("phone"),
                    "email": data.get("email")
                },
                "immunization": {
                    "vaccine_code": data.get("vaccineCode"),
                    "vaccine_name": data.get("vaccineName"),
                    "status": data.get("status", "completed"),
                    "date_administered": data.get("administrationDate"),
                    "lot_number": data.get("lotNumber")
                }
            }
            return result
        except Exception as e:
            raise ValueError(f"Error parsing JSON data: {str(e)}")

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
            birth_date=patient_data.get("birth_date"),
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
            date_administered=datetime.strptime(imm_data.get("date_administered"), "%Y-%m-%d").date()
                if imm_data.get("date_administered") else None,
            lot_number=imm_data.get("lot_number"),
            site=imm_data.get("site"),
            route=imm_data.get("route"),
            dose_quantity=imm_data.get("dose_quantity"),
            notes=imm_data.get("notes")
        )