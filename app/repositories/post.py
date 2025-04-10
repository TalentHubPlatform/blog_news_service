from core.utils.repository import CachedRepository
from blog_service.app.database.models.post import Post


class PostRepository(CachedRepository):
    model = Post