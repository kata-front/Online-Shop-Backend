from uuid import UUID
import httpx

class CatalogClient:
    def __init__(self, url: str):
        self.url = url

    async def get_product(self, id: UUID) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.url}/product/{id}")
        return response.json()