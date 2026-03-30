from pydantic import BaseModel, Field, BeforeValidator
from datetime import datetime
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class EventCreateRequest(BaseModel):
    title: str
    venue: str
    date: datetime
    total_seats: int
    price_per_seat: float


class EventUpdateRequest(BaseModel):
    title: str | None = None
    venue: str | None = None
    date: datetime | None = None
    total_seats: int | None = None
    price_per_seat: float | None = None


class EventResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    venue: str
    date: datetime  # TODO: While creating event, right now the date is current date time, make it user input
    organizer_id: str
    total_seats: int
    price_per_seat: float
    available_seats: int | None = None

    class Config:
        from_attributes = True
        populate_by_name = True
