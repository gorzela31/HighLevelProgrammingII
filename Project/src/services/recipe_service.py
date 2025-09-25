from typing import List, Optional
from ..models import Recipe
from ..db import Database, RecipeRepository


class RecipeService:
    """Application service for Recipe aggregate."""

    def __init__(self, repo: RecipeRepository):
        self.repo = repo

    # High-level API
    def add(self, recipe: Recipe) -> int:
        return self.repo.add(recipe)

    def get(self, recipe_id: int) -> Optional[Recipe]:
        return self.repo.get(recipe_id)

    def list_tags(self) -> list[str]:
        return self.repo.list_tags()

    def delete(self, recipe_id: int) -> None:
        self.repo.delete(recipe_id)

    def update(self, recipe: Recipe) -> None:
        self.repo.update(recipe)

    def set_favorite(self, recipe_id: int, fav: bool) -> None:
        self.repo.set_favorite(recipe_id, fav)

    def list_all(self) -> List[Recipe]:
        return self.repo.list_all()

    def list_favorites(self) -> List[Recipe]:
        return self.repo.list_favorites()

    def search(
        self,
        q: str = "",
        max_time: Optional[int] = None,
        only_fav: bool = False,
        tag: Optional[str] = None,
    ) -> list[Recipe]:
        return self.repo.search(q, max_time, only_fav, tag)

    def count(self) -> int:
        return self.repo.count()

    def count_favorites(self) -> int:
        return self.repo.count_favorites()

    def avg_prep_time(self) -> Optional[float]:
        return self.repo.avg_prep_time()


# Composition root used by Streamlit UI
def get_recipe_service(db_path: str) -> RecipeService:
    db = Database(db_path)
    db.init_schema()
    repo = RecipeRepository(db)
    return RecipeService(repo)
