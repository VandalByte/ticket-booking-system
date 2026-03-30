from pydantic import BaseModel, Field, BeforeValidator
from datetime import datetime
from enum import Enum
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class BookingCreateRequest(BaseModel):
    event_id: str
    seat_numbers: list[str]


class BookingResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    user_id: str
    event_id: str
    seat_numbers: list[str]
    status: BookingStatus
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class BookingStatusUpdate(BaseModel):
    status: BookingStatus
