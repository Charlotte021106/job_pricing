from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from job_pricing.services.feature_service import fetch_features_1d
from job_pricing.services.pricing_service import pricing_by_features
from job_pricing.db.mysql import mysql_get_baseline

router = APIRouter()

class QuoteReq(BaseModel):
    job_id: Optional[int] = None
    company_id: Optional[int] = None
    brand_factor: float = 1.0
    brand_level: Optional[float] = None
    top_talent_ratio: float = 0.10
    roi_target: float = 3.0
    v: float = 100.0

@router.post("/api/pricing/quote")
def quote(req: QuoteReq):
    online_price = None

    if req.job_id is not None:
        features = fetch_features_1d(req.job_id)
        if features:
            if req.brand_level is not None:
                brand_level = req.brand_level
            else:
                brand_level = 3.0 + (req.brand_factor - 1.0) / 0.05

            online_price = pricing_by_features(
                features,
                brand_level=brand_level,
                top_talent_ratio=req.top_talent_ratio,
                roi_target=req.roi_target,
                v=req.v,
            )

    row, baseline_price, _, _ = mysql_get_baseline(
        job_id=req.job_id, company_id=req.company_id
    )

    if online_price is not None:
        return {"price": online_price, "baseline_price": baseline_price}

    return {"price": baseline_price, "baseline_price": baseline_price}
