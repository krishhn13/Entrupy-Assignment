from fastapi import FastAPI, Depends, Request

from app.api.refresh import router as refresh_router
from app.api.products import router as products_router
from app.api.analytics import router as analytics_router
from app.api.notifications import router as notification_router
from app.api.meta import router as meta_router

from app.core.auth import verify_api_key

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
        title="Price Monitoring System",
        dependencies=[Depends(verify_api_key)]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
                "http://localhost:3000",
                "http://127.0.0.1:3000"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(refresh_router)
app.include_router(products_router)
app.include_router(analytics_router)
app.include_router(notification_router)
app.include_router(meta_router)


@app.get("/")
def root():
        return {"status" : "Price Monitoring API running"}

