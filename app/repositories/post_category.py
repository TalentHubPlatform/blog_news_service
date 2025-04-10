from core.utils.repository import CachedRepository
from app.database.models.category import PostCategory


class PostCategoryRepository(CachedRepository):
    model = PostCategory