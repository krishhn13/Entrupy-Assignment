from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.notification_service import dispatch_notifications

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/dispatch")
def dispatch(db: Session = Depends(get_db)):
        dispatch_notifications(db)
        return {
                "status" : "notification dispatched"
        }

