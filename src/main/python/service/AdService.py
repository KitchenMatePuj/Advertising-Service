from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from src.main.python.models.Ad import Ad
from src.main.python.repository.AdRepository import (
    create_ad,
    get_ad_by_id,
    list_all_ads,
    update_ad,
    delete_ad
)
from src.main.python.transformers.AdTransformer import (
    AdTransformer,
    AdResponse
)

def create_new_ad(db: Session, ad_data: dict) -> AdResponse:
    try:
        ad_entity = Ad(**ad_data)
        created = create_ad(db, ad_entity)
        return AdTransformer.to_response_model(created)
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
            detail={"error": "Unexpected error creating ad", "details": str(e)}
        )

def get_ad(db: Session, ad_id: int) -> AdResponse:
    try:
        ad = get_ad_by_id(db, ad_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        return AdTransformer.to_response_model(ad)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def list_ads(db: Session) -> List[AdResponse]:
    try:
        ads = list_all_ads(db)
        return [AdTransformer.to_response_model(a) for a in ads]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error listing ads", "details": str(e)}
        )

def modify_ad(db: Session, ad_id: int, ad_data: dict) -> AdResponse:
    try:
        ad = get_ad_by_id(db, ad_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Ad not found")

        for key, value in ad_data.items():
            if value is not None:
                setattr(ad, key, value)

        updated = update_ad(db, ad)
        return AdTransformer.to_response_model(updated)
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
            detail={"error": "Error updating ad", "details": str(e)}
        )

def remove_ad(db: Session, ad_id: int) -> dict:
    try:
        ad = get_ad_by_id(db, ad_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        delete_ad(db, ad)
        return {"message": "Ad successfully deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Error deleting ad", "details": str(e)}
        )
