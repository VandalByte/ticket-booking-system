from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.event_schema import EventCreateRequest
from datetime import datetime
import uuid


class EventRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["events"]

    async def create_event(self, event_data: EventCreateRequest, organizer_id: str):
        event_dict = event_data.model_dump()
        event_dict["_id"] = str(uuid.uuid4())
        event_dict["organizer_id"] = organizer_id
        event_dict["created_at"] = datetime.utcnow()

        await self.collection.insert_one(event_dict)
        return event_dict

    async def get_all_events(self):
        return await self.collection.find().to_list(length=100)

    async def get_event_by_id(self, event_id: str):
        """
        Finds a single event by its unique ID.
        """
        return await self.collection.find_one({"_id": event_id})
