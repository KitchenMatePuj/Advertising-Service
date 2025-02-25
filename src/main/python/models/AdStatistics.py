from sqlalchemy import Column, Integer, ForeignKey, DateTime
from src.main.python.models import Base
from datetime import datetime


class AdStatistics(Base):
    __tablename__ = "ad_statistics"

    stats_id = Column(Integer, primary_key=True, index=True)
    ad_id = Column(Integer, ForeignKey("ad.ad_id"), nullable=False)
    clicks = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
