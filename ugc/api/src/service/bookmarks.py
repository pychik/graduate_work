from datetime import datetime
from http import HTTPStatus

from db.mongo import get_mongo
from fastapi import Depends, HTTPException
from models.models import FilmBookmarks
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError


class BookmarksService:
    """
    Класс обрабатывает закладки пользователей.
    :Methods:
        - save - Создания новой закладки, (user_id, movie_id) должны быть уникальными.
        - delete - Удаление существующей закладки.
        - get_list - Возвращает список существующих закладок пользователя.
    :Parameters:
        - client - Клиент MongoDB(AsyncIOMotorClient)

    """
    def __init__(self, client: AsyncIOMotorClient):
        self.db = client['films']
        self.collection = self.db.get_collection("bookmarks")

    async def save(self, user_id: int, movie_id: str):
        # Create new bookmark.
        if not user_id or not movie_id:
            return

        document = dict(user_id=user_id, movie_id=movie_id, created_at=datetime.utcnow())
        try:
            doc = await self.collection.insert_one(document)
            if doc.inserted_id:
                doc = await self.collection.find_one({'_id': doc.inserted_id})
                return FilmBookmarks(
                    user_id=doc['user_id'],
                    movie_id=doc['movie_id'],
                    created_at=doc['created_at']
                )
        except DuplicateKeyError:
            msg = 'Record user_id - {user_id} and movie_id {movie_id} already exists!'
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=msg.format(user_id=user_id, movie_id=movie_id)
            )

    async def delete(self, user_id: int, movie_id: str):
        # Remove users bookmark.
        if not user_id or not movie_id:
            return

        data = {"user_id": user_id, "movie_id": movie_id}
        obj = await self.collection.find_one_and_delete(data, projection={"_id": False})

        if obj:
            return FilmBookmarks.parse_obj(obj)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Bookmark not found!')

    async def get_list(self, user_id: int):
        # Return list bookmarks.
        if not user_id:
            return

        query = {'user_id': user_id}
        return [FilmBookmarks(**doc) async for doc in self.collection.find(query)]


def get_service(client: AsyncIOMotorClient = Depends(get_mongo)) -> BookmarksService:
    return BookmarksService(client)
