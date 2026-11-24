from uuid import UUID

import httpx


class OrderClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_order(self, order_id: UUID):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/orders/{str(order_id)}")

        if response.status_code == 404:
            return None

        return response.json()