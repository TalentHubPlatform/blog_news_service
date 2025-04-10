from . import post
from . import comment
from . import tag
from . import post_tag
from . import category
from . import post_category

PostRepository = post.PostRepository
CommentRepository = comment.CommentRepository
TagRepository = tag.TagRepository
PostTagRepository = post_tag.PostTagRepository
CategoryRepository = category.CategoryRepository
PostCategoryRepository = post_category.PostCategoryRepository

__all__ = [
    "PostRepository",
    "CommentRepository",
    "TagRepository",
    "PostTagRepository",
    "CategoryRepository",
    "PostCategoryRepository",
]