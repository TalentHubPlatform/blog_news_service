
from core.utils.repository import CachedRepository
from app.database.models.tag import PostTag


class PostTagRepository(CachedRepository):
    model = PostTag