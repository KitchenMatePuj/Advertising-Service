from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.AdStatisticsService import (
    create_new_ad_statistics,
    get_ad_statistics,
    list_ad_statistics,
    modify_ad_statistics,
    remove_ad_statistics
)
from src.main.python.transformers.AdStatisticsTransformer import AdStatisticsResponse

router = APIRouter(prefix="/adstatistics", tags=["AdStatistics"])

@router.post("/", response_model=AdStatisticsResponse)
def create_ad_stats_endpoint(data: dict, db: Session = Depends(get_db)):
    return create_new_ad_statistics(db, data)

@router.get("/", response_model=List[AdStatisticsResponse])
def list_all_ad_stats_endpoint(db: Session = Depends(get_db)):
    return list_ad_statistics(db)

@router.get("/{stats_id}", response_model=AdStatisticsResponse)
def get_ad_stats_endpoint(stats_id: int, db: Session = Depends(get_db)):
    return get_ad_statistics(db, stats_id)

@router.put("/{stats_id}", response_model=AdStatisticsResponse)
def update_ad_stats_endpoint(stats_id: int, data: dict, db: Session = Depends(get_db)):
    return modify_ad_statistics(db, stats_id, data)

@router.delete("/{stats_id}", status_code=204)
def delete_ad_stats_endpoint(stats_id: int, db: Session = Depends(get_db)):
    remove_ad_statistics(db, stats_id)
    return
