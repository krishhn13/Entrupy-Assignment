import httpx
from sqlalchemy.orm import Session
from app.models.notification_event import NoticationEvent

WEBHOOK_URL = "https://webhook.site/test-endpoint"

def dispatch_notifications(db: Session):

        pending_events = (
                db.query(NoticationEvent).filter(NoticationEvent.status == "pending").all()
        )

        for event in pending_events:
                payload = {
                        "product_id" : str(event.product_id),
                        "old_price" : event.old_price,
                        "new_price" : event.new_price,
                }

                try: 
                        response = httpx.post(WEBHOOK_URL, json = payload)
                        
                        if response.status_code == 200:
                                event.status = "sent"
                        else :
                                event.retry_count+=1
                except Exception:
                        event.retry_count+=1
        
        db.commit()