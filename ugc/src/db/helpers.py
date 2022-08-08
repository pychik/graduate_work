from db.mongo import get_mongo
from pymongo import ASCENDING


async def create_indexes():
    client = await get_mongo()
    db = client['films']
    db.bookmarks.create_index([("user_id", ASCENDING), ("movie_id", ASCENDING)], unique=True)
