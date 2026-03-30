from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from datetime import datetime
from typing import Annotated

# Converts the MongoDB _id (if it's an ObjectId or string) to a string
PyObjectId = Annotated[str, BeforeValidator(str)]


class UserResponse(BaseModel):
    # Use Field(alias="_id") to tell Pydantic to look for "_id" in the DB
    # but show it as "id" in the JSON response
    id: PyObjectId = Field(alias="_id")
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True  # This allows using 'id' or '_id' during initialization


class UserUpdateRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
