from fastapi import FastAPI

from app.api.refresh import router as refresh_router

app = FastAPI(title="Price Monitoring System")

app.include_router(refresh_router)

@app.get("/")
def root():
        return {"status" : "Price Monitoring API running"}

