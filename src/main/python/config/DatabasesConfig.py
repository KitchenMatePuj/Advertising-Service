from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.python.ApplicationProperties import ApplicationProperties

props = ApplicationProperties()

DATABASE_URL = props.database_url
POOL_SIZE = props.database_pool_size

engine = create_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    echo=False
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
