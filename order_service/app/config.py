from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    db_url: str = 'postgresql+asyncpg://orders:orders@orders-db:5432/orders'
    catalog_url: str = "http://catalog-service:8000"

settings = Settings()