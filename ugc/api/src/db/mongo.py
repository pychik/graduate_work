from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

mongo: Optional[AsyncIOMotorClient] = None


async def get_mongo() -> AsyncIOMotorClient:
    return mongo
