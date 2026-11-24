from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .config import settings
from .clients.order_client import OrderClient
from .service import PaymentService

def get_order_client(base_url: str = settings.order_base_uri):
    return OrderClient(base_url)

def get_payment_service(
    db: AsyncSession = Depends(get_db),
    order_client: OrderClient = Depends(get_order_client)
):
    return PaymentService(db, order_client)