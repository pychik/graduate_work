import datetime
from functools import lru_cache

from fastapi import Depends
from models.models import FilmInfo, FilmRate, FilmReview, FilmReviewInfo
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from db.mongo import get_mongo



class RatingService:
    """Service for working with film rating (likes and reviews)."""

    def __init__(self, mongo: AsyncIOMotorClient):
        self.database = mongo.films
        self.rates_collection = self.database.get_collection("rates")
        self.reviews_collection = self.database.get_collection("reviews")

    async def get_film_info(self, film_id: str) -> FilmInfo or None:
        """Get film info with film_id [movie_id][likes][dislikes][rating]"""

        film = await self.rates_collection.find_one({"movie_id": film_id})
        if not film:
            return None
        like = await self.rates_collection.count_documents(
            {"$and": [{"movie_id": film_id}, {"rating": {"$gt": 4}}]}
        )
        dislike = await self.rates_collection.count_documents(
            {"$and": [{"movie_id": film_id}, {"rating": {"$lt": 5}}]}
        )
        cursor = self.rates_collection.aggregate(
            [
                {"$match": {"movie_id": film_id}},
                {"$group": {"_id": 0, "total": {"$sum": "$rating"}}},
            ]
        )
        search_result = await cursor.to_list(length=None)
        if search_result:
            avg = search_result[0]["total"] / (like + dislike)
        else:
            avg = 0.0
        return FilmInfo(movie_id=film_id, likes=like, dislikes=dislike, rating=avg)

    async def update_film_rate(self, film_id: str, user_id: str, rating: int) -> FilmRate or None:
        """Update user rate  with film_id and user_id."""
        filtered = {"user_id": user_id, "movie_id": film_id}
        updated = {"user_id": user_id, "movie_id": film_id, "rating": rating}

        replaced_rate = await self.rates_collection.find_one_and_replace(
            filtered,
            updated,
            projection={"_id": False},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )
        if replaced_rate:
            return FilmRate.parse_obj(replaced_rate)

    async def remove_film_rate(self, film_id: str, user_id: str) -> FilmRate or None:
        """Remove user rate with film_id and user id."""
        payload = {"user_id": user_id, "movie_id": film_id}
        removed_rate = await self.rates_collection.find_one_and_delete(
            payload, projection={"_id": False}
        )
        if removed_rate:
            return FilmRate.parse_obj(removed_rate)

    async def get_film_review_info(
        self, film_id: str, user_id: str
    ) -> FilmReviewInfo or None:
        """Get film review [movie_id][user_id][text][timestamp][rating]"""

        filtered = {"user_id": user_id, "movie_id": film_id}
        review = await self.reviews_collection.find_one(filtered)
        if not review:
            return None
        rates = await self.rates_collection.find_one(filtered)
        rating = None
        if rates:
            rating = rates["rating"]
        return FilmReviewInfo(
            movie_id=review["movie_id"],
            user_id=review["user_id"],
            text=review["text"],
            timestamp=review["timestamp"],
            rating=rating,
        )

    async def update_film_review(
        self, film_id: str, user_id: str, text: str, timestamp: datetime.datetime
    ) -> FilmReview:
        """Update film review"""
        filtered = {"user_id": user_id, "movie_id": film_id}
        updated = {
            "user_id": user_id,
            "movie_id": film_id,
            "text": text,
            "timestamp": timestamp,
        }
        updated_review = await self.reviews_collection.find_one_and_replace(
            filtered,
            updated,
            projection={"_id": False},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )
        if updated_review:
            return FilmReview.parse_obj(updated_review)

    async def remove_film_review(
        self, film_id: str, user_id: str
    ) -> FilmReview or None:
        """Remove film review with user_id and movie_id."""
        filtered = {"user_id": user_id, "movie_id": film_id}
        removed_review = await self.reviews_collection.find_one_and_delete(
            filtered, projection={"_id": False}
        )
        if removed_review:
            return FilmReview.parse_obj(removed_review)


@lru_cache()
def get_rating_service(
    mongo: AsyncIOMotorClient = Depends(get_mongo)
) -> RatingService:
    return RatingService(mongo)
