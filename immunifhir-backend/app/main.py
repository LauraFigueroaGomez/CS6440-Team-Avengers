from fastapi import FastAPI
from app.routes import patients, immunizations, mock_state, providers

app = FastAPI(title="ImmuniFHIR Backend")

app.include_router(patients.router,      prefix="/patients",      tags=["Patients"])
app.include_router(providers.router,     prefix="/providers",     tags=["Providers"])
app.include_router(immunizations.router, prefix="/immunizations", tags=["Immunizations"])
app.include_router(mock_state.router,    prefix="/mock",          tags=["Mock Registries"])
# app.include_router(aggregate.router,     prefix="/aggregate",     tags=["Aggregation"])

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
