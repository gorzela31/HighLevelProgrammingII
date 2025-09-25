from typing import List, Optional
from ..models import Recipe
from ..db import Database, RecipeRepository


class RecipeService:
    """Serwis aplikacyjny do zarządzania przepisami."""

    def __init__(self, repo: RecipeRepository):
        """Inicjalizuje serwis na podanym repozytorium."""
        self.repo = repo

    # High-level API
    def add(self, recipe: Recipe) -> int:
        """Dodaje przepis i zwraca jego ID."""
        return self.repo.add(recipe)

    def get(self, recipe_id: int) -> Optional[Recipe]:
        """Zwraca przepis po ID lub None."""
        return self.repo.get(recipe_id)

    def list_tags(self) -> list[str]:
        """Zwraca listę unikalnych tagów."""
        return self.repo.list_tags()

    def delete(self, recipe_id: int) -> None:
        """Usuwa przepis po ID."""
        self.repo.delete(recipe_id)

    def update(self, recipe: Recipe) -> None:
        """Aktualizuje dane przepisu."""
        self.repo.update(recipe)

    def set_favorite(self, recipe_id: int, fav: bool) -> None:
        """Ustawia/usuwa flagę ulubionego."""
        self.repo.set_favorite(recipe_id, fav)

    def list_all(self) -> List[Recipe]:
        """Zwraca wszystkie przepisy, najnowsze pierwsze."""
        return self.repo.list_all()

    def list_favorites(self) -> List[Recipe]:
        """Zwraca wszystkie ulubione przepisy."""
        return self.repo.list_favorites()

    def search(
        self,
        q: str = "",
        max_time: Optional[int] = None,
        only_fav: bool = False,
        tag: Optional[str] = None,
    ) -> list[Recipe]:
        """Wyszukuje przepisy według tekstu, czasu, ulubionych i tagu."""
        return self.repo.search(q, max_time, only_fav, tag)

    def count(self) -> int:
        """Zwraca liczbę wszystkich przepisów."""
        return self.repo.count()

    def count_favorites(self) -> int:
        """Zwraca liczbę ulubionych przepisów."""
        return self.repo.count_favorites()

    def avg_prep_time(self) -> Optional[float]:
        """Zwraca średni czas przygotowania (minuty), jeśli istnieje."""
        return self.repo.avg_prep_time()


# Composition root used by Streamlit UI
def get_recipe_service(db_path: str) -> RecipeService:
    """Buduje i zwraca skonfigurowany obiekt `RecipeService`."""
    db = Database(db_path)
    db.init_schema()
    repo = RecipeRepository(db)
    return RecipeService(repo)
