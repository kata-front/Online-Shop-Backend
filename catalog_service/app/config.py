from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_url: str = 'postgresql+asyncpg://catalog:catalog@catalog-db:5432/catalog'

settings=Settings()