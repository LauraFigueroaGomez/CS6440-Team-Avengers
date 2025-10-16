from fastapi import FastAPI
from app.routes import patients, immunizations, mock_state

app = FastAPI(title="ImmuniFHIR Backend")

app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(immunizations.router, prefix="/immunizations", tags=["Immunizations"])
app.include_router(mock_state.router, prefix="/mock", tags=["Mock Registries"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
