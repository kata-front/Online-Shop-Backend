from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db

from .service import CatalogService


def get_catalog_service(db: AsyncSession = Depends(get_db)):
    return CatalogService(
        db=db,
    )