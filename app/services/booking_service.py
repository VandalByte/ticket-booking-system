from fastapi import HTTPException
from redis import Redis


class BookingService:
    def __init__(self, booking_repo, seat_repo, event_repo, redis_client: Redis):
        self.booking_repo = booking_repo
        self.seat_repo = seat_repo
        self.event_repo = event_repo
        self.redis = redis_client

    async def initiate_booking(
        self, user_id: str, event_id: str, seat_numbers: list[str]
    ):
        # Verify Redis Lock exists for this user
        for seat in seat_numbers:
            lock_owner = self.redis.get(f"lock:{event_id}:{seat}")
            if lock_owner != user_id:
                raise HTTPException(
                    status_code=403,
                    detail=f"Lock expired or not owned by you for seat {seat}",
                )

        # Get Event details for pricing
        event = await self.event_repo.get_event_by_id(event_id)
        total_price = len(seat_numbers) * event["price_per_seat"]

        # Create Booking
        return await self.booking_repo.create_booking(
            user_id, event_id, seat_numbers, total_price
        )
