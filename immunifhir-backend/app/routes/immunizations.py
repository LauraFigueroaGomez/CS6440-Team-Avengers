from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Get immunization records")
def get_immunizations():
    return {"message": "Immunizations route working!"}
