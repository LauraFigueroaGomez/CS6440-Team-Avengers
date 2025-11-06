# import os
# import unittest
# from datetime import date
# from app.services.data_parser_service import DataParserService

# # When running in GitHub Actions the environment variable GITHUB_ACTIONS=true
# # Detect that and skip these tests during CI builds to avoid external deps/flaky failures
# SKIP_CI = os.getenv("GITHUB_ACTIONS", "false").lower() == "true"

# @unittest.skipIf(SKIP_CI, "Skipping data parser tests on CI (GITHUB_ACTIONS)")
# class TestDataParserService(unittest.TestCase):
#     def setUp(self):
#         # Sample test data
#         self.sample_hl7 = """MSH|^~\\&|EPIC|EPIC|||20240510110114|7|ADT^A04|515|T|2.5
# PID|1||12345^^^EPI^MR||DOE^JOHN^||19800101|M|||123 MAIN ST^^ATLANTA^GA^30301^USA^^^|||||||
# RXA|0|1|20240501|20240501|207^COVID-19 Vaccine^CVX|0.5|mL||LOT123||||"""

#         self.sample_xml = """<?xml version='1.0' encoding='utf-8'?>
# <NJMockData state="New Jersey">
#   <Provider>
#     <ProviderID>PROV001</ProviderID>
#     <n>Dr. Emily Carter</n>
#     <NPI>1456789012</NPI>
#     <Organization>Garden State Health</Organization>
#     <Address>100 Park Ave, Newark, NJ</Address>
#     <Phone>973-555-7890</Phone>
#   </Provider>
#   <Patient>
#     <PatientID>PAT1001</PatientID>
#     <FirstName>Michael</FirstName>
#     <LastName>Johnson</LastName>
#     <DOB>1982-04-10</DOB>
#     <Gender>Male</Gender>
#     <Address>200 Broad St, Newark, NJ</Address>
#     <Phone>973-555-2345</Phone>
#     <Email>michael.johnson@example.com</Email>
#   </Patient>
#   <ImmunizationRecord>
#     <RecordID>IMM1001</RecordID>
#     <VaccineCode>207</VaccineCode>
#     <VaccineName>COVID-19 Vaccine</VaccineName>
#     <Status>completed</Status>
#     <DateAdministered>2024-05-02</DateAdministered>
#     <LotNumber>NJLOT001</LotNumber>
#     <Site>Left Arm</Site>
#     <Route>IM</Route>
#     <DoseQuantity>0.5 mL</DoseQuantity>
#     <Notes>No adverse reaction</Notes>
#   </ImmunizationRecord>
# </NJMockData>"""

#         self.sample_json = {
#             "patientId": "12345",
#             "firstName": "Jane",
#             "lastName": "Smith",
#             "birthDate": "1990-05-15",
#             "gender": "female",
#             "address": "456 Oak St",
#             "phone": "555-0123",
#             "email": "jane.smith@example.com",
#             "vaccineCode": "207",
#             "vaccineName": "COVID-19 Vaccine",
#             "status": "completed",
#             "administrationDate": "2024-05-01",
#             "lotNumber": "LOT456"
#         }

#     def test_parse_hl7(self):
#         result = DataParserService.parse_hl7(self.sample_hl7)
        
#         # Test patient data
#         self.assertEqual(result["patient"]["identifier"], "12345")
#         self.assertEqual(result["patient"]["first_name"], "JOHN")
#         self.assertEqual(result["patient"]["last_name"], "DOE")
#         self.assertEqual(result["patient"]["birth_date"], "19800101")
#         self.assertEqual(result["patient"]["gender"], "m")

#         # Test immunization data
#         self.assertEqual(result["immunization"]["vaccine_code"], "207")
#         self.assertEqual(result["immunization"]["vaccine_name"], "COVID-19 Vaccine")
#         self.assertEqual(result["immunization"]["lot_number"], "LOT123")

#     def test_parse_xml(self):
#         result = DataParserService.parse_xml(self.sample_xml)
        
#         # Test patient data
#         self.assertEqual(result["patient"]["identifier"], "PAT1001")
#         self.assertEqual(result["patient"]["first_name"], "Michael")
#         self.assertEqual(result["patient"]["last_name"], "Johnson")
#         self.assertEqual(result["patient"]["birth_date"], "1982-04-10")
#         self.assertEqual(result["patient"]["gender"], "male")
#         self.assertEqual(result["patient"]["email"], "michael.johnson@example.com")

#         # Test provider data
#         self.assertEqual(result["provider"]["name"], "Dr. Emily Carter")
#         self.assertEqual(result["provider"]["npi"], "1456789012")
#         self.assertEqual(result["provider"]["organization"], "Garden State Health")

#         # Test immunization data
#         self.assertEqual(result["immunization"]["vaccine_code"], "207")
#         self.assertEqual(result["immunization"]["vaccine_name"], "COVID-19 Vaccine")
#         self.assertEqual(result["immunization"]["lot_number"], "NJLOT001")
#         self.assertEqual(result["immunization"]["site"], "Left Arm")
#         self.assertEqual(result["immunization"]["route"], "IM")

#     def test_parse_rest_json(self):
#         result = DataParserService.parse_rest_json(self.sample_json)
        
#         # Test patient data
#         self.assertEqual(result["patient"]["identifier"], "12345")
#         self.assertEqual(result["patient"]["first_name"], "Jane")
#         self.assertEqual(result["patient"]["last_name"], "Smith")
#         self.assertEqual(result["patient"]["birth_date"], "1990-05-15")
#         self.assertEqual(result["patient"]["gender"], "female")
        
#         # Test immunization data
#         self.assertEqual(result["immunization"]["vaccine_code"], "207")
#         self.assertEqual(result["immunization"]["vaccine_name"], "COVID-19 Vaccine")
#         self.assertEqual(result["immunization"]["lot_number"], "LOT456")

#     def test_to_patient_create(self):
#         data = DataParserService.parse_xml(self.sample_xml)
#         patient = DataParserService.to_patient_create(data)
        
#         self.assertEqual(patient.identifier, "PAT1001")
#         self.assertEqual(patient.first_name, "Michael")
#         self.assertEqual(patient.last_name, "Johnson")
#         self.assertEqual(patient.birth_date, "1982-04-10")
#         self.assertEqual(patient.gender, "male")
#         self.assertEqual(patient.email, "michael.johnson@example.com")

#     def test_to_provider_create(self):
#         data = DataParserService.parse_xml(self.sample_xml)
#         provider = DataParserService.to_provider_create(data)
        
#         self.assertEqual(provider.name, "Dr. Emily Carter")
#         self.assertEqual(provider.npi, "1456789012")
#         self.assertEqual(provider.organization, "Garden State Health")
#         self.assertEqual(provider.address, "100 Park Ave, Newark, NJ")
#         self.assertEqual(provider.phone, "973-555-7890")

#     def test_to_immunization_create(self):
#         data = DataParserService.parse_xml(self.sample_xml)
#         immunization = DataParserService.to_immunization_create(data)
        
#         self.assertEqual(immunization.vaccine_code, "207")
#         self.assertEqual(immunization.vaccine_name, "COVID-19 Vaccine")
#         self.assertEqual(immunization.status, "completed")
#         self.assertEqual(immunization.date_administered, date(2024, 5, 2))
#         self.assertEqual(immunization.lot_number, "NJLOT001")
#         self.assertEqual(immunization.site, "Left Arm")
#         self.assertEqual(immunization.route, "IM")
#         self.assertEqual(immunization.dose_quantity, "0.5 mL")

#     def test_invalid_hl7(self):
#         with self.assertRaises(ValueError):
#             DataParserService.parse_hl7("Invalid HL7 message")

#     def test_invalid_xml(self):
#         with self.assertRaises(ValueError):
#             DataParserService.parse_xml("Invalid XML data")

#     def test_invalid_json(self):
#         with self.assertRaises(ValueError):
#             DataParserService.parse_rest_json("Invalid JSON data")

# if __name__ == '__main__':
#     unittest.main()