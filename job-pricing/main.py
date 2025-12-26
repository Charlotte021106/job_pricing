import os
from dotenv import load_dotenv
from fastapi import FastAPI
from job_pricing.routers.pricing import router as pricing_router

load_dotenv()
app = FastAPI(title="Job Pricing API", version="0.4.3")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(pricing_router)
