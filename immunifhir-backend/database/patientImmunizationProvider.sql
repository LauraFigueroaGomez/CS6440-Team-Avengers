INSERT INTO Providers (name, npi, organization, address, phone)
VALUES ('Dr. Sarah Thompson', '1234567890', 'WellHealth Clinic', '123 Main St, Albany, NY', '555-123-4567');
INSERT INTO Patients (identifier, first_name, last_name, birth_date, gender, address, phone, email)
VALUES ('PAT001', 'John', 'Doe', '1985-06-15', 'male', '456 Elm St, Albany, NY', '555-987-6543', 'john.doe@example.com');
INSERT INTO ImmunizationRecords (
  patient_id,
  provider_id,
  vaccine_code,
  vaccine_name,
  status,
  date_administered,
  lot_number,
  site,
  route,
  dose_quantity,
  notes
)
VALUES (
  (SELECT id FROM Patients WHERE identifier = 'PAT001'),
  (SELECT id FROM Providers WHERE npi = '1234567890'),
  '207',
  'COVID-19 Vaccine',
  'completed',
  '2024-05-01',
  'LOT12345',
  'Left Arm',
  'IM',
  '0.5 mL',
  'No adverse reaction'
);
