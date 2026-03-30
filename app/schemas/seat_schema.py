from pydantic import BaseModel, Field, BeforeValidator
from enum import Enum
from typing import Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]


class SeatStatus(str, Enum):
    available = "available"
    locked = "locked"
    booked = "booked"


class SeatResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    event_id: str
    seat_number: str
    status: SeatStatus

    class Config:
        from_attributes = True
        populate_by_name = True


class SeatLockRequest(BaseModel):
    event_id: str
    seat_numbers: list[str]


class SeatReleaseRequest(BaseModel):
    event_id: str
    seat_numbers: list[str]
