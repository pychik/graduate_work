from abc import ABC, abstractmethod


class AsyncCacheService(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass


class AsyncSearchService(ABC):
    @abstractmethod
    async def get(self, index, id, doc_type=None, params=None, headers=None):
        pass

    @abstractmethod
    async def search(
            self, body=None, index=None, doc_type=None, params=None, headers=None
    ):
        pass
