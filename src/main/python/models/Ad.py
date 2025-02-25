from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from src.main.python.models import Base

class Ad(Base):
    __tablename__ = "ad"

    ad_id = Column(Integer, primary_key=True, index=True)
    advertiser_id = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    start_date = Column(DateTime, default=None, nullable=True)
    end_date = Column(DateTime, default=None, nullable=True)
