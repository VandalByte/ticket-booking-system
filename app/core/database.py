from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import redis


class Database:
    client: AsyncIOMotorClient = None
    db = None
    redis_client = None


db_helper = Database()


async def connect_to_mongo():
    db_helper.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_helper.db = db_helper.client[settings.DATABASE_NAME]
    print("Connected to MongoDB")
    db_helper.redis_client = redis.Redis(
        host="localhost", port=6379, db=0, decode_responses=True
    )
    print("Connected to Redis")


async def close_mongo_connection():
    db_helper.client.close()
    print("Closed MongoDB connection")


def get_db():
    return db_helper.db


def get_redis():
    return db_helper.redis_client
