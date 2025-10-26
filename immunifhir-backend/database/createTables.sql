-- 1. Patients
CREATE TABLE IF NOT EXISTS Patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  identifier TEXT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  birth_date DATE,
  gender TEXT,
  address TEXT,
  phone TEXT,
  email TEXT
);

-- 2. Providers
CREATE TABLE IF NOT EXISTS Providers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  npi TEXT,
  organization TEXT,
  address TEXT,
  phone TEXT
);

-- 3. ImmunizationRecords
CREATE TABLE IF NOT EXISTS ImmunizationRecords (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID REFERENCES Patients(id),
  provider_id UUID REFERENCES Providers(id),
  vaccine_code TEXT,
  vaccine_name TEXT,
  status TEXT,
  date_administered DATE,
  lot_number TEXT,
  expiration_date DATE,
  site TEXT,
  route TEXT,
  dose_quantity TEXT,
  notes TEXT
);
