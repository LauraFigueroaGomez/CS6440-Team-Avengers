from fastapi import APIRouter

router = APIRouter()

@router.get("/ny", summary="Mock NY - HL7")
def mock_ny():
    hl7_records = [
        # Original sample
        (
            "MSH|^~\\&|NYSIIS|NY||Clinic|20241012||VXU^V04|MSG1|P|2.5.1\r"
            "PID|1||12345^^^NY^MR||DOE^JOHN||19800210|M\r"
            "RXA|0|1|20241012||140^Influenza, seasonal^CVX|0.5|mL||GSK12345||||||||LOT999\r"
        ),

        "MSH|^~\\&|NYSIIS|NY||Clinic|20241013||VXU^V04|MSG2|P|2.5.1\rPID|1||23456^^^NY^MR||SMITH^JANE||19910522|F\rRXA|0|1|20241013||207^COVID-19 Vaccine^CVX|0.5|mL||PFZ12345||||||||LOT888\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241014||VXU^V04|MSG3|P|2.5.1\rPID|1||34567^^^NY^MR||LEE^DAVID||19881230|M\rRXA|0|1|20241014||33^MMR^CVX|0.5|mL||MRK12345||||||||LOT777\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241015||VXU^V04|MSG4|P|2.5.1\rPID|1||45678^^^NY^MR||PATEL^PRIYA||20000101|F\rRXA|0|1|20241015||140^Influenza, seasonal^CVX|0.5|mL||GSK54321||||||||LOT666\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241016||VXU^V04|MSG5|P|2.5.1\rPID|1||56789^^^NY^MR||GARCIA^LUIS||19751111|M\rRXA|0|1|20241016||88^Tetanus-diphtheria^CVX|0.5|mL||TDX12345||||||||LOT555\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241017||VXU^V04|MSG6|P|2.5.1\rPID|1||67890^^^NY^MR||KIM^SOO||19990303|F\rRXA|0|1|20241017||49^Polio^CVX|0.5|mL||POL12345||||||||LOT444\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241018||VXU^V04|MSG7|P|2.5.1\rPID|1||78901^^^NY^MR||BROWN^SAMUEL||19860606|M\rRXA|0|1|20241018||140^Influenza, seasonal^CVX|0.5|mL||GSK67890||||||||LOT333\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241019||VXU^V04|MSG8|P|2.5.1\rPID|1||89012^^^NY^MR||WILSON^OLIVIA||20021212|F\rRXA|0|1|20241019||207^COVID-19 Vaccine^CVX|0.5|mL||PFZ67890||||||||LOT222\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241020||VXU^V04|MSG9|P|2.5.1\rPID|1||90123^^^NY^MR||ZHANG^LI||19970707|M\rRXA|0|1|20241020||33^MMR^CVX|0.5|mL||MRK67890||||||||LOT111\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241021||VXU^V04|MSG10|P|2.5.1\rPID|1||12321^^^NY^MR||SINGH^ANITA||19830303|F\rRXA|0|1|20241021||140^Influenza, seasonal^CVX|0.5|mL||GSK11111||||||||LOT000\r",
        "MSH|^~\\&|NYSIIS|NY||Clinic|20241022||VXU^V04|MSG11|P|2.5.1\rPID|1||32123^^^NY^MR||MARTINEZ^CARLOS||19791209|M\rRXA|0|1|20241022||88^Tetanus-diphtheria^CVX|0.5|mL||TDX54321||||||||LOT999\r"
    ]
    return {"source": "NY", "format": "HL7", "data": hl7_records}

@router.get("/nj", summary="Mock NJ - XML")
def mock_nj():
    xml_records = [
        # Original sample
        "<Immunization><PatientId>67890</PatientId><Vaccine>Influenza</Vaccine><Date>2024-10-12</Date></Immunization>",

        "<Immunization><PatientId>10001</PatientId><Vaccine>COVID-19</Vaccine><Date>2024-10-13</Date></Immunization>",
        "<Immunization><PatientId>10002</PatientId><Vaccine>MMR</Vaccine><Date>2024-10-14</Date></Immunization>",
        "<Immunization><PatientId>10003</PatientId><Vaccine>Influenza</Vaccine><Date>2024-10-15</Date></Immunization>",
        "<Immunization><PatientId>10004</PatientId><Vaccine>Tetanus-diphtheria</Vaccine><Date>2024-10-16</Date></Immunization>",
        "<Immunization><PatientId>10005</PatientId><Vaccine>Polio</Vaccine><Date>2024-10-17</Date></Immunization>",
        "<Immunization><PatientId>10006</PatientId><Vaccine>Influenza</Vaccine><Date>2024-10-18</Date></Immunization>",
        "<Immunization><PatientId>10007</PatientId><Vaccine>COVID-19</Vaccine><Date>2024-10-19</Date></Immunization>",
        "<Immunization><PatientId>10008</PatientId><Vaccine>MMR</Vaccine><Date>2024-10-20</Date></Immunization>",
        "<Immunization><PatientId>10009</PatientId><Vaccine>Influenza</Vaccine><Date>2024-10-21</Date></Immunization>",
        "<Immunization><PatientId>10010</PatientId><Vaccine>Tetanus-diphtheria</Vaccine><Date>2024-10-22</Date></Immunization>"
    ]
    return {"source": "NJ", "format": "XML", "data": xml_records}

@router.get("/pa", summary="Mock PA - JSON")
def mock_pa():
    json_records = [
        # Original sample
        {"patient_id":"24680","vaccine":"MMR","date":"2024-10-12"},

        {"patient_id":"10001","vaccine":"COVID-19","date":"2024-10-13"},
        {"patient_id":"10002","vaccine":"MMR","date":"2024-10-14"},
        {"patient_id":"10003","vaccine":"Influenza","date":"2024-10-15"},
        {"patient_id":"10004","vaccine":"Tetanus-diphtheria","date":"2024-10-16"},
        {"patient_id":"10005","vaccine":"Polio","date":"2024-10-17"},
        {"patient_id":"10006","vaccine":"Influenza","date":"2024-10-18"},
        {"patient_id":"10007","vaccine":"COVID-19","date":"2024-10-19"},
        {"patient_id":"10008","vaccine":"MMR","date":"2024-10-20"},
        {"patient_id":"10009","vaccine":"Influenza","date":"2024-10-21"},
        {"patient_id":"10010","vaccine":"Tetanus-diphtheria","date":"2024-10-22"}
    ]
    return {"source": "PA", "format": "JSON", "data": json_records}
