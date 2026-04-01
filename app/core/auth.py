from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.api_key import APIKey
from app.models.api_usage import APIUsage


async def verify_api_key(request: Request):

    api_key = request.headers.get("x-api-key")

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    db: Session = SessionLocal()

    key_exists = (
        db.query(APIKey)
        .filter(APIKey.key == api_key)
        .first()
    )

    if not key_exists:
        db.close()
        raise HTTPException(status_code=403, detail="Invalid API key")

    usage = APIUsage(
        api_key=api_key,
        endpoint=request.url.path,
    )

    db.add(usage)
    db.commit()
    db.close()