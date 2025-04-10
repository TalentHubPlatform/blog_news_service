from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.database.schemas.post import PostCreate, PostUpdate, PostStatus
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any


class PostService:
    async def create_post(self, uow: AbstractUnitOfWork, post: PostCreate):
        post_dict = post.model_dump(exclude_none=True)

        async with uow:
            post_id = await uow.posts.add_one(post_dict)
            return post_id

    async def get_post_by_id(self, uow: AbstractUnitOfWork, post_id: int):
        async with uow:
            post = await uow.posts.find_one({"id": post_id})
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post #{post_id} not found."
                )
            return post

    async def get_posts(self, uow: AbstractUnitOfWork, filters: Optional[Dict[str, Any]] = None):
        if filters is None:
            filters = {}

        async with uow:
            posts = await uow.posts.find_some(filters)
            return posts

    async def get_posts_by_author(self, uow: AbstractUnitOfWork, author_id: int):
        async with uow:
            posts = await uow.posts.find_some({"author_id": author_id})
            return posts

    async def get_published_posts(self, uow: AbstractUnitOfWork):
        async with uow:
            posts = await uow.posts.find_some({"status": PostStatus.PUBLISHED})
            return posts

    async def update_post(self, uow: AbstractUnitOfWork, post_id: int, post_update: PostUpdate):
        await self.get_post_by_id(uow, post_id)

        post_dict = post_update.model_dump(exclude_unset=True)

        async with uow:
            updated_post = await uow.posts.update({"id": post_id}, post_dict)
            return updated_post

    async def delete_post(self, uow: AbstractUnitOfWork, post_id: int):
        await self.get_post_by_id(uow, post_id)

        async with uow:
            deleted_post = await uow.posts.delete({"id": post_id})
            return deleted_post

    async def publish_post(self, uow: AbstractUnitOfWork, post_id: int):
        await self.get_post_by_id(uow, post_id)

        async with uow:
            published_post = await uow.posts.update(
                {"id": post_id},
                {"status": PostStatus.PUBLISHED}
            )
            return published_post

    async def archive_post(self, uow: AbstractUnitOfWork, post_id: int):
        await self.get_post_by_id(uow, post_id)

        async with uow:
            archived_post = await uow.posts.update(
                {"id": post_id},
                {"status": PostStatus.ARCHIVED}
            )
            return archived_post

    async def add_tag_to_post(self, uow: AbstractUnitOfWork, post_id: int, tag_id: int):
        await self.get_post_by_id(uow, post_id)

        async with uow:
            tag = await uow.tags.find_one({"id": tag_id})
            if not tag:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag #{tag_id} not found."
                )

            existing_relation = await uow.post_tags.find_one({
                "post_id": post_id,
                "tag_id": tag_id
            })
            if existing_relation:
                return existing_relation

            relation = await uow.post_tags.add_one({
                "post_id": post_id,
                "tag_id": tag_id
            })
            return relation

    async def remove_tag_from_post(self, uow: AbstractUnitOfWork, post_id: int, tag_id: int):
        await self.get_post_by_id(uow, post_id)

        async with uow:
            result = await uow.post_tags.delete({
                "post_id": post_id,
                "tag_id": tag_id
            })
            return result

    async def add_category_to_post(self, uow: AbstractUnitOfWork, post_id: int, category_id: int):
        await self.get_post_by_id(uow, post_id)

        async with uow:
            category = await uow.categories.find_one({"id": category_id})
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category #{category_id} not found."
                )

            existing_relation = await uow.post_categories.find_one({
                "post_id": post_id,
                "category_id": category_id
            })
            if existing_relation:
                return existing_relation

            relation = await uow.post_categories.add_one({
                "post_id": post_id,
                "category_id": category_id
            })
            return relation

    async def remove_category_from_post(self, uow: AbstractUnitOfWork, post_id: int, category_id: int):
        await self.get_post_by_id(uow, post_id)

        async with uow:
            result = await uow.post_categories.delete({
                "post_id": post_id,
                "category_id": category_id
            })
            return result