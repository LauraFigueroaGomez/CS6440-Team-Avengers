import { getAuthToken, logout } from './auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

if (!API_BASE_URL) {
  console.warn('VITE_API_BASE_URL is not defined in .env')
}

// Build query string from an object
const buildQueryString = (params = {}) =>
  Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&')

export const apiRequest = async (method, path, { params, body } = {}) => {
  const token = await getAuthToken()
  console.log("TOKEN?", token ? "yes" : "no")

  let url = `${API_BASE_URL}${path}`
  const qs = buildQueryString(params)
  if (qs) url += `?${qs}`

  const headers = { "Content-Type": "application/json" }
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(url, { method, headers, ...(body ? { body: JSON.stringify(body) } : {}) })

  const text = await res.text()   // read as text first

  if (!res.ok) {
    // show real backend error text (HTML or JSON)
    throw new Error(`HTTP ${res.status}: ${text}`)
  }

  // try parsing JSON only if it looks like JSON
  try {
    return JSON.parse(text)
  } catch {
    throw new Error(`Expected JSON but got: ${text.slice(0, 120)}...`)
  }
}

// GET /patients/search
export const searchPatients = async ({ firstName, lastName, dob }) => {
  const data = await apiRequest('GET', '/patients/search', {
    params: {
      first_name: firstName,
      last_name: lastName,
      birth_date: dob
    }
  })

  // Return exactly what the backend gives you, but converted to frontend naming
  return data.map(p => ({
    id: p.id,
    mrn: p.identifier,
    firstName: p.first_name,
    lastName: p.last_name,
    dob: p.birth_date,
    gender: p.gender,
    address: p.address,

    recordCount: p.immunization_count
  }))
}

// GET /patients/{id} -> { patient, immunizations, state_summary }
const computeAge = (dobStr) => {
  if (!dobStr) return null
  const today = new Date()
  const dob = new Date(dobStr)
  let age = today.getFullYear() - dob.getFullYear()
  const m = today.getMonth() - dob.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
    age--
  }
  return age
}

export const getPatientDetails = async (id) => {
  // Get patient core demographics
  const p = await apiRequest('GET', `/patients/${id}`)

  // Get immunizations for that patient
  const immunizations = await apiRequest(
    'GET',
    `/immunizations/by-patient/${id}`
  )

  // Build state summary (by state/source_state)
  const stateSummary = {}
  ;(immunizations || []).forEach((im) => {
    const state = im.source_state || 'Unknown'
    if (!stateSummary[state]) {
      stateSummary[state] = { count: 0, lastUpdate: null }
    }
    stateSummary[state].count += 1

    const d = im.date_administered
    if (!stateSummary[state].lastUpdate || d > stateSummary[state].lastUpdate) {
      stateSummary[state].lastUpdate = d
    }
  })

  // Map backend fields into what the Vue component expects
  const mappedImmunizations = (immunizations || []).map((im) => ({
    date: im.date_administered,
    vaccine: im.vaccine_name,
    manufacturer: im.manufacturer || '',
    dose: im.dose_quantity || '',
    lot: im.lot_number || im.id,
    provider: im.provider_name || '',
    location: im.site || '',
    state: im.source_state || '',
    status: im.status || 'completed'
  }))

  return {
    id: p.id,
    mrn: p.identifier,
    firstName: p.first_name,
    lastName: p.last_name,
    dob: p.birth_date,
    age: computeAge(p.birth_date),
    gender: p.gender,
    address: p.address,
    immunizations: mappedImmunizations,
    stateSummary
  }
}
