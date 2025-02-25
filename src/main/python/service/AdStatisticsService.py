from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.main.python.models.AdStatistics import AdStatistics
from src.main.python.repository.AdStatisticsRepository import (
    create_ad_statistics,
    get_ad_statistics_by_id,
    list_all_ad_statistics,
    update_ad_statistics,
    delete_ad_statistics
)
from src.main.python.transformers.AdStatisticsTransformer import (
    AdStatisticsTransformer,
    AdStatisticsResponse
)

def create_new_ad_statistics(db: Session, stats_data: dict) -> AdStatisticsResponse:
    try:
        stats_entity = AdStatistics(**stats_data)
        created = create_ad_statistics(db, stats_entity)
        return AdStatisticsTransformer.to_response_model(created)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database integrity error", "details": str(e.__cause__)}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Unexpected error creating ad statistics", "details": str(e)}
        )

def get_ad_statistics(db: Session, stats_id: int) -> AdStatisticsResponse:
    try:
        stats = get_ad_statistics_by_id(db, stats_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Ad statistics record not found")
        return AdStatisticsTransformer.to_response_model(stats)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def list_ad_statistics(db: Session) -> List[AdStatisticsResponse]:
    try:
        stats_list = list_all_ad_statistics(db)
        return [AdStatisticsTransformer.to_response_model(s) for s in stats_list]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error listing ad statistics", "details": str(e)}
        )

def modify_ad_statistics(db: Session, stats_id: int, data: dict) -> AdStatisticsResponse:
    try:
        stats = get_ad_statistics_by_id(db, stats_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Ad statistics record not found")

        for key, value in data.items():
            if value is not None:
                setattr(stats, key, value)

        updated = update_ad_statistics(db, stats)
        return AdStatisticsTransformer.to_response_model(updated)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Database integrity error", "details": str(e.__cause__)}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error updating ad statistics", "details": str(e)}
        )

def remove_ad_statistics(db: Session, stats_id: int) -> dict:
    try:
        stats = get_ad_statistics_by_id(db, stats_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Ad statistics record not found")
        delete_ad_statistics(db, stats)
        return {"message": "Ad statistics record successfully deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error deleting ad statistics", "details": str(e)}
        )
