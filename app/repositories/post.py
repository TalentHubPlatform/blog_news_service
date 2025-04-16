from app.core.utils.repository import CachedRepository
from app.database.models.post import Post


class PostRepository(CachedRepository):
    model = Post