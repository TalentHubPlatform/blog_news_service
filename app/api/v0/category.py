from typing import List, Optional

from app.api.dependencies import UOWAlchemyDep
from app.core.auth import get_current_user
from app.database.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategorySchema,
    CategoryWithPostsCountSchema,
)
from app.database.schemas.post import PostSchema
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.services.category import CategoryService

category_router = APIRouter()


@category_router.get("/", response_model=List[CategorySchema])
async def get_categories(uow: UOWAlchemyDep):
    return await CategoryService().get_categories(uow)


@category_router.get("/with-count", response_model=List[CategoryWithPostsCountSchema])
async def get_categories_with_count(uow: UOWAlchemyDep):
    return await CategoryService().get_categories_with_posts_count(uow)


@category_router.get("/{category_id}", response_model=CategorySchema)
async def get_category_by_id(uow: UOWAlchemyDep, category_id: int):
    return await CategoryService().get_category_by_id(uow, category_id)


@category_router.get("/name/{category_name}", response_model=CategorySchema)
async def get_category_by_name(uow: UOWAlchemyDep, category_name: str):
    category = await CategoryService().get_category_by_name(uow, category_name)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with name '{category_name}' not found",
        )
    return category


@category_router.get("/{category_id}/posts", response_model=List[PostSchema])
async def get_posts_by_category(uow: UOWAlchemyDep, category_id: int):
    return await CategoryService().get_posts_by_category(uow, category_id)


@category_router.post("/", response_model=int)
async def create_category(
    uow: UOWAlchemyDep, category: CategoryCreate, current_user=Depends(get_current_user)
):
    if current_user.role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only editors can create categories",
        )

    return await CategoryService().create_category(uow, category)


@category_router.patch("/{category_id}", response_model=CategorySchema)
async def update_category(
    uow: UOWAlchemyDep,
    category_id: int,
    category: CategoryUpdate,
    current_user=Depends(get_current_user),
):
    if current_user.role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only editors can update categories",
        )

    return await CategoryService().update_category(uow, category_id, category)


@category_router.delete("/{category_id}", response_model=CategorySchema)
async def delete_category(
    uow: UOWAlchemyDep, category_id: int, current_user=Depends(get_current_user)
):
    if current_user.role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only editors can delete categories",
        )

    return await CategoryService().delete_category(uow, category_id)