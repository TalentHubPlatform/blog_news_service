from fastapi import APIRouter

from app.api.v0.post import post_router
from app.api.v0.comment import comment_router
from app.api.v0.tag import tag_router
from app.api.v0.category import category_router

main_v0_router = APIRouter(prefix="/api/v0")
main_v0_router.include_router(post_router, prefix="/post", tags=["post"])
main_v0_router.include_router(comment_router, prefix="/comment", tags=["comment"])
main_v0_router.include_router(tag_router, prefix="/tag", tags=["tag"])
main_v0_router.include_router(category_router, prefix="/category", tags=["category"])