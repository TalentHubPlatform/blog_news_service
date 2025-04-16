from app.core.utils.repository import CachedRepository
from app.database.models.comment import Comment


class CommentRepository(CachedRepository):
    model = Comment