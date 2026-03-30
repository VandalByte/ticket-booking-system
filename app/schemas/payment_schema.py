from pydantic import BaseModel, Field, BeforeValidator
from datetime import datetime
from enum import Enum
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class PaymentStatus(str, Enum):
    success = "success"
    failed = "failed"
    pending = "pending"


class PaymentCreateRequest(BaseModel):
    booking_id: str
    amount: float
    payment_method: str = "card"  # card | upi | netbanking


class PaymentResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    booking_id: str
    amount: float
    status: PaymentStatus
    payment_method: str
    payment_time: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
