from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.database.schemas.tag import TagCreate, TagUpdate
from fastapi import HTTPException, status


class TagService:
    async def create_tag(self, uow: AbstractUnitOfWork, tag: TagCreate):
        existing_tag = await self.get_tag_by_name(uow, tag.name)
        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tag with name '{tag.name}' already exists."
            )

        tag_dict = tag.model_dump(exclude_none=True)

        async with uow:
            tag_id = await uow.tags.add_one(tag_dict)
            return tag_id

    async def get_tag_by_id(self, uow: AbstractUnitOfWork, tag_id: int):
        async with uow:
            tag = await uow.tags.find_one({"id": tag_id})
            if not tag:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag #{tag_id} not found."
                )
            return tag

    async def get_tag_by_name(self, uow: AbstractUnitOfWork, name: str):
        async with uow:
            tag = await uow.tags.find_one({"name": name})
            return tag

    async def get_tags(self, uow: AbstractUnitOfWork):
        async with uow:
            tags = await uow.tags.find_all()
            return tags

    async def update_tag(self, uow: AbstractUnitOfWork, tag_id: int, tag_update: TagUpdate):
        await self.get_tag_by_id(uow, tag_id)

        if tag_update.name:
            existing_tag = await self.get_tag_by_name(uow, tag_update.name)
            if existing_tag and existing_tag.id != tag_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Tag with name '{tag_update.name}' already exists."
                )

        tag_dict = tag_update.model_dump(exclude_unset=True)

        async with uow:
            updated_tag = await uow.tags.update({"id": tag_id}, tag_dict)
            return updated_tag

    async def delete_tag(self, uow: AbstractUnitOfWork, tag_id: int):
        await self.get_tag_by_id(uow, tag_id)

        async with uow:
            deleted_tag = await uow.tags.delete({"id": tag_id})
            return deleted_tag

    async def get_posts_by_tag(self, uow: AbstractUnitOfWork, tag_id: int):
        await self.get_tag_by_id(uow, tag_id)

        async with uow:
            relations = await uow.post_tags.find_some({"tag_id": tag_id})

            post_ids = [relation.post_id for relation in relations]

            if not post_ids:
                return []

            posts = []
            for post_id in post_ids:
                post = await uow.posts.find_one({"id": post_id})
                if post:
                    posts.append(post)

            return posts

    async def get_popular_tags(self, uow: AbstractUnitOfWork, limit: int = 10):
        async with uow:
            tags = await uow.tags.find_all()

            tags_with_count = []
            for tag in tags:
                relations = await uow.post_tags.find_some({"tag_id": tag.id})
                tag_data = {
                    "id": tag.id,
                    "name": tag.name,
                    "posts_count": len(relations)
                }
                tags_with_count.append(tag_data)

            sorted_tags = sorted(tags_with_count, key=lambda x: x["posts_count"], reverse=True)

            return sorted_tags[:limit]