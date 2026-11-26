from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from .service import OrderService
from .database import get_db
from .clients.payment_client import PaymentClient
from .clients.catalog_client import CatalogClient
from .config import settings

def get_catalog_client(base_url: str = settings.catalog_url):
    return CatalogClient(base_url)

def get_payment_client(base_url: str = settings.payment_url):
    return PaymentClient(base_url)

def get_order_service(
    db: AsyncSession = Depends(get_db),
    catalog_client: CatalogClient = Depends(get_catalog_client),
    payment_client: PaymentClient = Depends(get_payment_client)
):
    return OrderService(db, catalog_client, payment_client)