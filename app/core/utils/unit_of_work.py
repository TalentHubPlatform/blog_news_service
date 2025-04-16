from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING

import fakeredis
from app.database.redis import RedisSingleton
from app.database.session import get_db
from fakeredis import TcpFakeServer
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.utils import SQLAlchemyRepository
from app.core.utils.cache import RedisCache
from app.core.utils.repository import AbstractRepository

if TYPE_CHECKING:
    from app.repositories.post import PostRepository
    from app.repositories.comment import CommentRepository
    from app.repositories.tag import TagRepository
    from app.repositories.post_tag import PostTagRepository
    from app.repositories.category import CategoryRepository
    from app.repositories.post_category import PostCategoryRepository


class AbstractUnitOfWork(ABC):
    batches: AbstractRepository

    @abstractmethod
    def __init__(self, session_factory):
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class CachedSQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory=Depends(get_db),
    ):
        self.session_factory = session_factory
        self.redis = fakeredis.FakeAsyncRedis()

    def get_repository(self, repo_class):
        return repo_class(
            repository=SQLAlchemyRepository(self.session), cache=RedisCache(self.redis)
        )

    async def __aenter__(self):
        self.session: AsyncSession = await anext(self.session_factory())

        from app.repositories.post import PostRepository
        from app.repositories.comment import CommentRepository
        from app.repositories.tag import TagRepository
        from app.repositories.post_tag import PostTagRepository
        from app.repositories.category import CategoryRepository
        from app.repositories.post_category import PostCategoryRepository

        self.posts = self.get_repository(PostRepository)
        self.comments = self.get_repository(CommentRepository)
        self.tags = self.get_repository(TagRepository)
        self.post_tags = self.get_repository(PostTagRepository)
        self.categories = self.get_repository(CategoryRepository)
        self.post_categories = self.get_repository(PostCategoryRepository)

        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self.session:
                await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()