from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.database.schemas.category import CategoryCreate, CategoryUpdate
from fastapi import HTTPException, status


class CategoryService:
    async def create_category(self, uow: AbstractUnitOfWork, category: CategoryCreate):
        existing_category = await self.get_category_by_name(uow, category.name)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with name '{category.name}' already exists."
            )

        category_dict = category.model_dump(exclude_none=True)

        async with uow:
            category_id = await uow.categories.add_one(category_dict)
            return category_id

    async def get_category_by_id(self, uow: AbstractUnitOfWork, category_id: int):
        async with uow:
            category = await uow.categories.find_one({"id": category_id})
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category #{category_id} not found."
                )
            return category

    async def get_category_by_name(self, uow: AbstractUnitOfWork, name: str):
        async with uow:
            category = await uow.categories.find_one({"name": name})
            return category

    async def get_categories(self, uow: AbstractUnitOfWork):
        async with uow:
            categories = await uow.categories.find_all()
            return categories

    async def update_category(self, uow: AbstractUnitOfWork, category_id: int, category_update: CategoryUpdate):
        await self.get_category_by_id(uow, category_id)

        if category_update.name:
            existing_category = await self.get_category_by_name(uow, category_update.name)
            if existing_category and existing_category.id != category_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Category with name '{category_update.name}' already exists."
                )

        category_dict = category_update.model_dump(exclude_unset=True)

        async with uow:
            updated_category = await uow.categories.update({"id": category_id}, category_dict)
            return updated_category

    async def delete_category(self, uow: AbstractUnitOfWork, category_id: int):
        await self.get_category_by_id(uow, category_id)

        async with uow:
            deleted_category = await uow.categories.delete({"id": category_id})
            return deleted_category

    async def get_posts_by_category(self, uow: AbstractUnitOfWork, category_id: int):
        await self.get_category_by_id(uow, category_id)

        async with uow:
            relations = await uow.post_categories.find_some({"category_id": category_id})

            post_ids = [relation.post_id for relation in relations]

            if not post_ids:
                return []

            posts = []
            for post_id in post_ids:
                post = await uow.posts.find_one({"id": post_id})
                if post:
                    posts.append(post)

            return posts

    async def get_categories_with_posts_count(self, uow: AbstractUnitOfWork):
        async with uow:
            categories = await uow.categories.find_all()

            categories_with_count = []
            for category in categories:
                relations = await uow.post_categories.find_some({"category_id": category.id})
                category_data = {
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                    "posts_count": len(relations)
                }
                categories_with_count.append(category_data)

            return categories_with_count