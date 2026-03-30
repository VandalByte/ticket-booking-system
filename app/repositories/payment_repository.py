from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import uuid


class PaymentRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["payments"]

    async def create_payment_record(
        self, booking_id: str, amount: float, method: str, status: str
    ):
        payment_doc = {
            "_id": str(uuid.uuid4()),
            "booking_id": booking_id,
            "amount": amount,
            "payment_method": method,
            "status": status,
            "payment_time": datetime.now(timezone.utc),
        }
        await self.collection.insert_one(payment_doc)
        return payment_doc
