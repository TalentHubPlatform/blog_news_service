from app.core.utils.repository import CachedRepository
from app.database.models.tag import Tag


class TagRepository(CachedRepository):
    model = Tag