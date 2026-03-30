from motor.motor_asyncio import AsyncIOMotorDatabase


class SeatRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["seats"]

    async def bulk_create_seats(self, seats_list: list):
        """Inserts a list of seat documents in one go."""
        if seats_list:
            return await self.collection.insert_many(seats_list)
        return None

    async def get_seats_by_event(self, event_id: str):
        """Fetches all seats for a specific event."""
        return await self.collection.find({"event_id": event_id}).to_list(length=None)

    async def get_seat_by_number(self, event_id: str, seat_number: str):
        return await self.collection.find_one(
            {"event_id": event_id, "seat_number": seat_number}
        )

    async def mark_seats_booked(self, event_id: str, seat_numbers: list[str]):
        result = await self.collection.update_many(
            {
                "event_id": event_id,  # Must match exactly
                "seat_number": {"$in": seat_numbers},
            },
            {"$set": {"status": "booked"}},
        )
        # print(f"Updated {result.modified_count} seats")  # Debugging statement
        return result
