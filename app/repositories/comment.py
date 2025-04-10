from core.utils.repository import CachedRepository
from blog_service.app.database.models.comment import Comment


class CommentRepository(CachedRepository):
    model = Comment