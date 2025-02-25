from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.main.python.models.Ad import Ad

class AdResponse(BaseModel):
    ad_id: int
    advertiser_id: str
    content: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    class Config:
        orm_mode = True

class AdTransformer:
    @staticmethod
    def to_response_model(ad: Ad) -> AdResponse:
        return AdResponse(
            ad_id=ad.ad_id,
            advertiser_id=ad.advertiser_id,
            content=ad.content,
            start_date=ad.start_date,
            end_date=ad.end_date
        )
