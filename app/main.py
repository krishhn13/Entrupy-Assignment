from fastapi import FastAPI, Depends, Request

from app.api.refresh import router as refresh_router
from app.api.products import router as products_router
from app.api.analytics import router as analytics_router
from app.api.notifications import router as notification_router
from app.core.auth import verify_api_key

app = FastAPI(
        title="Price Monitoring System",
        dependencies=[Depends(verify_api_key)]
)

app.include_router(refresh_router)
app.include_router(products_router)
app.include_router(analytics_router)
app.include_router(notification_router)


@app.get("/")
def root():
        return {"status" : "Price Monitoring API running"}

