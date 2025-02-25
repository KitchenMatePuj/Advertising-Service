from fastapi import FastAPI
from src.main.python.config.DatabasesConfig import engine
from src.main.python.models import Base
from src.main.python.models.Ad import Base as AdBase
from src.main.python.models.AdStatistics import Base as StatsBase

from src.main.python.controller.AdController import router as ad_router
from src.main.python.controller.AdStatisticsController import router as stats_router

def create_app() -> FastAPI:
    app = FastAPI(title="Ads Microservice")

    Base.metadata.create_all(bind=engine)

    app.include_router(ad_router)
    app.include_router(stats_router)

    return app

app = create_app()
