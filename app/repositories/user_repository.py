from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.auth_schema import RegisterRequest
from datetime import datetime, timezone
import uuid


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def create_user(self, user_data: RegisterRequest, hashed_password: str):
        user_dict = {
            "_id": str(uuid.uuid4()),
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password,
            "role": user_data.role,
            "created_at": datetime.now(timezone.utc),
        }

        result = await self.collection.insert_one(user_dict)
        return user_dict

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})
