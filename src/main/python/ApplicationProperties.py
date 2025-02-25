import os

class ApplicationProperties:
    @property
    def database_url(self) -> str:
        return os.environ.get("DATABASE_URL", "mysql+pymysql://root:1234@localhost:3306/ads_db")

    @property
    def database_pool_size(self) -> int:
        return int(os.environ.get("DATABASE_POOL_SIZE", "5"))

    @property
    def log_level(self) -> str:
        return os.environ.get("LOG_LEVEL", "INFO")
