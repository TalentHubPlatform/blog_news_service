from typing import List

from app.api.dependencies import UOWAlchemyDep
from app.database.schemas.tag import (
    TagCreate,
    TagUpdate,
    TagSchema,
    TagWithPostsCountSchema,
)
from app.database.schemas.post import PostSchema
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.services.tag import TagService

tag_router = APIRouter()


@tag_router.get("/", response_model=List[TagSchema])
async def get_tags(uow: UOWAlchemyDep):
    return await TagService().get_tags(uow)


@tag_router.get("/popular", response_model=List[TagWithPostsCountSchema])
async def get_popular_tags(
    uow: UOWAlchemyDep, limit: int = Query(10, ge=1, le=100, description="Limit of tags to return")
):
    return await TagService().get_popular_tags(uow, limit)


@tag_router.get("/{tag_id}", response_model=TagSchema)
async def get_tag_by_id(uow: UOWAlchemyDep, tag_id: int):
    return await TagService().get_tag_by_id(uow, tag_id)


@tag_router.get("/name/{tag_name}", response_model=TagSchema)
async def get_tag_by_name(uow: UOWAlchemyDep, tag_name: str):
    tag = await TagService().get_tag_by_name(uow, tag_name)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with name '{tag_name}' not found",
        )
    return tag


@tag_router.get("/{tag_id}/posts", response_model=List[PostSchema])
async def get_posts_by_tag(uow: UOWAlchemyDep, tag_id: int):
    return await TagService().get_posts_by_tag(uow, tag_id)


@tag_router.post("/", response_model=int)
async def create_tag(uow: UOWAlchemyDep, tag: TagCreate):

    return await TagService().create_tag(uow, tag)


@tag_router.patch("/{tag_id}", response_model=TagSchema)
async def update_tag(
    uow: UOWAlchemyDep,
    tag_id: int,
    tag: TagUpdate
):

    return await TagService().update_tag(uow, tag_id, tag)


@tag_router.delete("/{tag_id}", response_model=TagSchema)
async def delete_tag(uow: UOWAlchemyDep, tag_id: int):

    return await TagService().delete_tag(uow, tag_id)
