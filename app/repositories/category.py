from app.core.utils.repository import CachedRepository
from app.database.models.category import Category


class CategoryRepository(CachedRepository):
    model = Category