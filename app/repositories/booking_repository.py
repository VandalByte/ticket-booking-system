from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import uuid


class BookingRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["bookings"]

    async def create_booking(
        self, user_id: str, event_id: str, seat_numbers: list[str], total_price: float
    ):
        booking_doc = {
            "_id": str(uuid.uuid4()),
            "user_id": user_id,
            "event_id": event_id,
            "seat_numbers": seat_numbers,
            "total_price": total_price,
            "status": "pending",  # pending -> confirmed/cancelled
            "created_at": datetime.now(timezone.utc),
        }
        await self.collection.insert_one(booking_doc)
        return booking_doc

    async def get_booking_by_id(self, booking_id: str):
        return await self.collection.find_one({"_id": booking_id})

    async def update_status(self, booking_id: str, status: str):
        result = await self.collection.update_one(
            {"_id": booking_id}, {"$set": {"status": status}}
        )
        # print(f"Updated {result.modified_count} booking")  # debugging statement
        return result
