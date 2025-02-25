from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from src.main.python.config.DatabasesConfig import get_db
from src.main.python.service.AdService import (
    create_new_ad,
    get_ad,
    list_ads,
    modify_ad,
    remove_ad
)
from src.main.python.transformers.AdTransformer import AdResponse

router = APIRouter(prefix="/ads", tags=["Ads"])

@router.post("/", response_model=AdResponse)
def create_ad_endpoint(ad_data: dict, db: Session = Depends(get_db)):
    return create_new_ad(db, ad_data)

@router.get("/", response_model=List[AdResponse])
def list_all_ads_endpoint(db: Session = Depends(get_db)):
    return list_ads(db)

@router.get("/{ad_id}", response_model=AdResponse)
def get_ad_endpoint(ad_id: int, db: Session = Depends(get_db)):
    return get_ad(db, ad_id)

@router.put("/{ad_id}", response_model=AdResponse)
def update_ad_endpoint(ad_id: int, ad_data: dict, db: Session = Depends(get_db)):
    return modify_ad(db, ad_id, ad_data)

@router.delete("/{ad_id}", status_code=204)
def delete_ad_endpoint(ad_id: int, db: Session = Depends(get_db)):
    remove_ad(db, ad_id)
    return
