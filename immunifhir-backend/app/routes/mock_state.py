from fastapi import APIRouter

router = APIRouter()

@router.get("/ny")
def mock_ny():
    return "MSH|^~\\&|NYSIIS|..."
