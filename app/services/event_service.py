from app.repositories.event_repository import EventRepository
from app.repositories.seat_repository import SeatRepository
from app.schemas.event_schema import EventCreateRequest
import uuid


class EventService:
    def __init__(self, event_repo: EventRepository, seat_repo: SeatRepository):
        self.event_repo = event_repo
        self.seat_repo = seat_repo

    async def create_event_with_seats(
        self, event_data: EventCreateRequest, organizer_id: str
    ):
        # Save event first
        new_event = await self.event_repo.create_event(event_data, organizer_id)
        event_id = new_event["_id"]

        # Logic to generate seat numbers (e.g., A1 to A20, B1 to B20...)
        seats_to_create = []
        rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        seats_per_row = event_data.total_seats // len(rows)

        for row in rows:
            for num in range(1, seats_per_row + 1):
                seat_doc = {
                    "_id": str(uuid.uuid4()),
                    "event_id": event_id,
                    "seat_number": f"{row}{num}",
                    "status": "available",  # available | locked | booked
                }
                seats_to_create.append(seat_doc)

        await self.seat_repo.bulk_create_seats(seats_to_create)

        return new_event
