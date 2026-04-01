from datetime import datetime, timedelta
import httpx

MAX_RETRIES = 5
BASE_DELAY_SECONDS = 10

from sqlalchemy.orm import Session
from app.models.notification_event import NotificationEvent


WEBHOOK_URL = "https://webhook.site/test-endpoint"


def dispatch_notifications(db: Session):

    now = datetime.utcnow()

    pending_events = (
        db.query(NotificationEvent)
        .filter(NotificationEvent.status == "pending")
        .filter(NotificationEvent.next_retry_at <= now)
        .all()
    )

    for event in pending_events:

        payload = {
            "product_id": str(event.product_id),
            "old_price": event.old_price,
            "new_price": event.new_price,
        }

        try:

            response = httpx.post(WEBHOOK_URL, json=payload)

            if response.status_code == 200:

                event.status = "sent"

            else:

                schedule_retry(event)

        except Exception:

            schedule_retry(event)

    db.commit()


def schedule_retry(event):

    event.retry_count += 1

    if event.retry_count >= MAX_RETRIES:

        event.status = "failed"
        return

    delay = BASE_DELAY_SECONDS * (2 ** event.retry_count)

    event.next_retry_at = datetime.utcnow() + timedelta(seconds=delay)