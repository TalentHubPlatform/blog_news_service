from typing import List

from app.api.dependencies import UOWAlchemyDep
from app.database.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentSchema,
    CommentDetailSchema,
)
from fastapi import APIRouter

from app.services.comment import CommentService
from app.services.post import PostService

comment_router = APIRouter()


@comment_router.get("/post/{post_id}", response_model=List[CommentSchema])
async def get_comments_by_post(uow: UOWAlchemyDep, post_id: int):
    await PostService().get_post_by_id(uow, post_id)

    return await CommentService().get_comments_by_post(uow, post_id)


@comment_router.get("/{comment_id}", response_model=CommentDetailSchema)
async def get_comment_by_id(uow: UOWAlchemyDep, comment_id: int):
    return await CommentService().get_comment_by_id(uow, comment_id)


@comment_router.get("/{comment_id}/replies", response_model=List[CommentSchema])
async def get_comment_replies(uow: UOWAlchemyDep, comment_id: int):
    await CommentService().get_comment_by_id(uow, comment_id)

    return await CommentService().get_replies(uow, comment_id)


@comment_router.post("/", response_model=int)
async def create_comment(
        uow: UOWAlchemyDep, comment: CommentCreate):
    return await CommentService().create_comment(uow, comment)


@comment_router.patch("/{comment_id}", response_model=CommentSchema)
async def update_comment(
        uow: UOWAlchemyDep,
        comment_id: int,
        comment: CommentUpdate):
    existing_comment = await CommentService().get_comment_by_id(uow, comment_id)

    return await CommentService().update_comment(uow, comment_id, comment)


@comment_router.delete("/{comment_id}", response_model=CommentSchema)
async def delete_comment(
        uow: UOWAlchemyDep, comment_id: int):
    existing_comment = await CommentService().get_comment_by_id(uow, comment_id)

    return await CommentService().delete_comment(uow, comment_id)


@comment_router.patch("/{comment_id}/approve", response_model=CommentSchema)
async def approve_comment(
        uow: UOWAlchemyDep, comment_id: int):

    return await CommentService().approve_comment(uow, comment_id)


@comment_router.patch("/{comment_id}/reject", response_model=CommentSchema)
async def reject_comment(
        uow: UOWAlchemyDep, comment_id: int):

    return await CommentService().reject_comment(uow, comment_id)
