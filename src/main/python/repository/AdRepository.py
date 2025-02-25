from sqlalchemy.orm import Session
from src.main.python.models.Ad import Ad

def create_ad(db: Session, ad: Ad) -> Ad:
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad

def get_ad_by_id(db: Session, ad_id: int) -> Ad:
    return db.query(Ad).filter(Ad.ad_id == ad_id).first()

def list_all_ads(db: Session):
    return db.query(Ad).all()

def update_ad(db: Session, ad: Ad) -> Ad:
    db.commit()
    db.refresh(ad)
    return ad

def delete_ad(db: Session, ad: Ad) -> None:
    db.delete(ad)
    db.commit()
