from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import patients, immunizations, mock_state, providers, aggregate
from app.routes import fhir

app = FastAPI(title="ImmuniFHIR Backend")

origins = [
    "http://localhost:5173",
    "https://cs6440-team-avengers-1-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router,      prefix="/patients",      tags=["Patients"])
app.include_router(providers.router,     prefix="/providers",     tags=["Providers"])
app.include_router(immunizations.router, prefix="/immunizations", tags=["Immunizations"])
app.include_router(mock_state.router,    prefix="/mock",          tags=["Mock Registries"])
app.include_router(aggregate.router,     prefix="/aggregate",     tags=["Aggregation"])
app.include_router(fhir.router,          prefix="/fhir",          tags=["FHIR"])

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
