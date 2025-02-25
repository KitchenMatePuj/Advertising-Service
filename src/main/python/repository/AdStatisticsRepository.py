from sqlalchemy.orm import Session
from src.main.python.models.AdStatistics import AdStatistics

def create_ad_statistics(db: Session, stats: AdStatistics) -> AdStatistics:
    db.add(stats)
    db.commit()
    db.refresh(stats)
    return stats

def get_ad_statistics_by_id(db: Session, stats_id: int) -> AdStatistics:
    return db.query(AdStatistics).filter(AdStatistics.stats_id == stats_id).first()

def list_all_ad_statistics(db: Session):
    return db.query(AdStatistics).all()

def update_ad_statistics(db: Session, stats: AdStatistics) -> AdStatistics:
    db.commit()
    db.refresh(stats)
    return stats

def delete_ad_statistics(db: Session, stats: AdStatistics) -> None:
    db.delete(stats)
    db.commit()
