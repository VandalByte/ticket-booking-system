from fastapi import HTTPException, status
from redis import Redis
from app.repositories.seat_repository import SeatRepository


class SeatService:
    def __init__(self, seat_repo: SeatRepository, redis_client: Redis):
        self.seat_repo = seat_repo
        self.redis = redis_client

    async def lock_seats(self, event_id: str, seat_numbers: list[str], user_id: str):
        for seat in seat_numbers:
            lock_key = f"lock:{event_id}:{seat}"

            # Check if seat is already locked in Redis
            if self.redis.get(lock_key):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Seat {seat} is currently being held by another user.",
                )

            # Check MongoDB to ensure it's not already 'booked'
            db_seat = await self.seat_repo.get_seat_by_number(event_id, seat)
            if db_seat["status"] == "booked":
                raise HTTPException(
                    status_code=400, detail=f"Seat {seat} is already sold."
                )

        # If all clear, set locks in Redis with a 5-minute expiry (300 seconds)
        for seat in seat_numbers:
            lock_key = f"lock:{event_id}:{seat}"
            self.redis.set(lock_key, user_id, ex=300)

        return {"message": "Seats locked for 5 minutes", "seats": seat_numbers}
