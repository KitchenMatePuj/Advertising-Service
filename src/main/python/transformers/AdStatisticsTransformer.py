from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.main.python.models.AdStatistics import AdStatistics

class AdStatisticsResponse(BaseModel):
    stats_id: int
    ad_id: int
    clicks: int
    impressions: int
    updated_at: datetime

    class Config:
        orm_mode = True

class AdStatisticsTransformer:
    @staticmethod
    def to_response_model(stats: AdStatistics) -> AdStatisticsResponse:
        return AdStatisticsResponse(
            stats_id=stats.stats_id,
            ad_id=stats.ad_id,
            clicks=stats.clicks,
            impressions=stats.impressions,
            updated_at=stats.updated_at
        )
