from typing import Optional, List, Dict, Any

from app.api.dependencies import UOWAlchemyDep
from app.database.schemas.post import (
    PostCreate,
    PostUpdate,
    PostSchema,
    PostDetailSchema,
)
from app.database.schemas.pagination import PaginationParams
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.services.post import PostService

post_router = APIRouter()


@post_router.get("/", response_model=List[PostSchema])
async def get_posts(
    uow: UOWAlchemyDep,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    search: Optional[str] = None,
    type: Optional[str] = None,
    status: Optional[str] = None,
):
    filters = {}
    if type:
        filters["type"] = type
    if status:
        filters["status"] = status

    pagination_params = PaginationParams(
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search,
    )

    return await PostService().get_posts(uow, filters)


@post_router.get("/{post_id}", response_model=PostDetailSchema)
async def get_post_by_id(uow: UOWAlchemyDep, post_id: int):
    return await PostService().get_post_by_id(uow, post_id)


@post_router.get("/author/{author_id}", response_model=List[PostSchema])
async def get_posts_by_author(uow: UOWAlchemyDep, author_id: int):
    return await PostService().get_posts_by_author(uow, author_id)


@post_router.post("/", response_model=int)
async def create_post(
    uow: UOWAlchemyDep, post: PostCreate):


    return await PostService().create_post(uow, post)


@post_router.patch("/{post_id}", response_model=PostSchema)
async def update_post(
    uow: UOWAlchemyDep,
    post_id: int,
    post: PostUpdate,
):
    existing_post = await PostService().get_post_by_id(uow, post_id)

    return await PostService().update_post(uow, post_id, post)


@post_router.delete("/{post_id}", response_model=PostSchema)
async def delete_post(
    uow: UOWAlchemyDep, post_id: int):
    existing_post = await PostService().get_post_by_id(uow, post_id)

    return await PostService().delete_post(uow, post_id)


@post_router.patch("/{post_id}/publish", response_model=PostSchema)
async def publish_post(
    uow: UOWAlchemyDep, post_id: int):
    existing_post = await PostService().get_post_by_id(uow, post_id)

    return await PostService().publish_post(uow, post_id)


@post_router.patch("/{post_id}/archive", response_model=PostSchema)
async def archive_post(
    uow: UOWAlchemyDep, post_id: int):
    existing_post = await PostService().get_post_by_id(uow, post_id)

    return await PostService().archive_post(uow, post_id)


@post_router.post("/{post_id}/tags/{tag_id}", response_model=dict)
async def add_tag_to_post(
    uow: UOWAlchemyDep, post_id: int, tag_id: int):
    existing_post = await PostService().get_post_by_id(uow, post_id)

    return await PostService().add_tag_to_post(uow, post_id, tag_id)


@post_router.delete("/{post_id}/tags/{tag_id}", response_model=dict)
async def remove_tag_from_post(
    uow: UOWAlchemyDep, post_id: int, tag_id: int):
    existing_post = await PostService().get_post_by_id(uow, post_id)

    return await PostService().remove_tag_from_post(uow, post_id, tag_id)


@post_router.post("/{post_id}/categories/{category_id}", response_model=dict)
async def add_category_to_post(
    uow: UOWAlchemyDep, post_id: int, category_id: int):
    existing_post = await PostService().get_post_by_id(uow, post_id)

    return await PostService().add_category_to_post(uow, post_id, category_id)


@post_router.delete("/{post_id}/categories/{category_id}", response_model=dict)
async def remove_category_from_post(
    uow: UOWAlchemyDep, post_id: int, category_id: int):
    existing_post = await PostService().get_post_by_id(uow, post_id)

    return await PostService().remove_category_from_post(uow, post_id, category_id)
