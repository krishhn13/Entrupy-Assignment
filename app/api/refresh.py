from fastapi import APIRouter
from app.services.refresh_service import refresh_all_sources

router = APIRouter()

@router.post("/refresh")
def refresh_data():
        files_processed = refresh_all_sources()

        return {
                "status" : "refresh completed",
                "files_processed" : len(files_processed)
        }