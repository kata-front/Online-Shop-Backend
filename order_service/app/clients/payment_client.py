from uuid import UUID
import httpx

class PaymentClient:
    def __init__(self, url: str):
        self.url = url

    async def create_payment(self, order_id: UUID, user_id: UUID, amount: int) -> dict:
        json_data = {
            'order_id': str(order_id,),
            'user_id': str(user_id), 
            'amount': amount
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/payments/{order_id}",
                json=json_data
            )
        return response.json()