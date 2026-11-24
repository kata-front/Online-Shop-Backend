from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore'
    )

    db_url: str = 'postgresql+asyncpg://payments:payments@payments-db:5432/payments'
    order_base_uri: str = "http://order-service:8000"

settings = Settings()