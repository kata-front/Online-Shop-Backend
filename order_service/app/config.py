from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    db_url: str = 'postgresql+asyncpg://orders:orders@orders-db:5432/orders'
    catalog_url: str = "http://catalog-service:8000"
    payment_url: str = "http://payment-service:8000"

    rebbitmq_url: str = "amqp://guest:guest@rabbitmq:5672"
    payment_succeeded_routimg_key: str = 'payment.succeeded'
    payment_queue_name: str = 'orders.payments.results'
    payment_exchange_name: str = 'payment.events'

settings = Settings()