from fastapi import APIRouter

router = APIRouter()

@router.get("/ny", summary="Mock NY - HL7")
def mock_ny():
    hl7 = (
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241012||VXU^V04|MSG1|P|2.5.1\r"
        "PID|1||12345^^^NY^MR||DOE^JOHN||19800210|M\r"
        "RXA|0|1|20241012||140^Influenza, seasonal^CVX|0.5|mL||GSK12345||||||||LOT999\r"
    )
    return {"source": "NY", "format": "HL7", "data": hl7}

@router.get("/nj", summary="Mock NJ - XML")
def mock_nj():
    xml = "<Immunization><PatientId>67890</PatientId><Vaccine>Influenza</Vaccine><Date>2024-10-12</Date></Immunization>"
    return {"source": "NJ", "format": "XML", "data": xml}

@router.get("/pa", summary="Mock PA - JSON")
def mock_pa():
    return {"source": "PA", "format": "JSON", "data": {"patient_id":"24680","vaccine":"MMR","date":"2024-10-12"}}
