from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore'
    )

    db_url: str = 'postgresql+asyncpg://notifs:notifs@notifs-db:5432/notifs'
    rebbitmq_url: str = "amqp://guest:guest@rabbitmq:5672"

    payment_succeeded_routimg_key: str = 'payment.succeeded'
    payment_queue_name: str = 'notifs.payments.results'
    payment_exchange_name: str = 'payment.events'

settings = Settings()