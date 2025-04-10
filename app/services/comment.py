from app.core.utils.unit_of_work import AbstractUnitOfWork
from app.database.schemas.comment import CommentCreate, CommentUpdate
from fastapi import HTTPException, status


class CommentService:
    async def create_comment(self, uow: AbstractUnitOfWork, comment: CommentCreate):
        comment_dict = comment.model_dump(exclude_none=True)

        async with uow:
            post = await uow.posts.find_one({"id": comment.post_id})
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post #{comment.post_id} not found."
                )

            if comment.parent_id:
                parent_comment = await uow.comments.find_one({"id": comment.parent_id})
                if not parent_comment:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Parent comment #{comment.parent_id} not found."
                    )

                if parent_comment.post_id != comment.post_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Parent comment belongs to a different post."
                    )

            comment_id = await uow.comments.add_one(comment_dict)
            return comment_id

    async def get_comment_by_id(self, uow: AbstractUnitOfWork, comment_id: int):
        async with uow:
            comment = await uow.comments.find_one({"id": comment_id})
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Comment #{comment_id} not found."
                )
            return comment

    async def get_comments_by_post(self, uow: AbstractUnitOfWork, post_id: int):
        async with uow:
            comments = await uow.comments.find_some({"post_id": post_id})
            return comments

    async def get_replies(self, uow: AbstractUnitOfWork, comment_id: int):
        async with uow:
            replies = await uow.comments.find_some({"parent_id": comment_id})
            return replies

    async def update_comment(self, uow: AbstractUnitOfWork, comment_id: int, comment_update: CommentUpdate):
        comment = await self.get_comment_by_id(uow, comment_id)

        comment_dict = comment_update.model_dump(exclude_unset=True)

        async with uow:
            updated_comment = await uow.comments.update({"id": comment_id}, comment_dict)
            return updated_comment

    async def delete_comment(self, uow: AbstractUnitOfWork, comment_id: int):
        await self.get_comment_by_id(uow, comment_id)

        async with uow:
            deleted_comment = await uow.comments.delete({"id": comment_id})
            return deleted_comment

    async def approve_comment(self, uow: AbstractUnitOfWork, comment_id: int):
        await self.get_comment_by_id(uow, comment_id)

        async with uow:
            approved_comment = await uow.comments.update(
                {"id": comment_id},
                {"is_approved": True}
            )
            return approved_comment

    async def reject_comment(self, uow: AbstractUnitOfWork, comment_id: int):
        await self.get_comment_by_id(uow, comment_id)

        async with uow:
            rejected_comment = await uow.comments.update(
                {"id": comment_id},
                {"is_approved": False}
            )
            return rejected_comment