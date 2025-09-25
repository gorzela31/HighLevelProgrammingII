import sqlite3
from typing import List, Optional
from .models import Recipe


class Database:
    """Wrapper na bazę SQLite."""

    def __init__(self, path: str):
        """Inicjalizuje obiekt bazy."""
        self.path = path

    def connect(self) -> sqlite3.Connection:
        """Zwraca nowe połączenie do bazy."""
        return sqlite3.connect(self.path)

    def init_schema(self) -> None:
        """Tworzy schemat tabeli `recipes`, jeśli nie istnieje."""
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    ingredients TEXT,
                    instructions TEXT,
                    prep_time_minutes INTEGER,
                    tags TEXT,
                    favorite INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()


class RecipeRepository:
    """Repozytorium odpowiedzialne za operacje na przepisach."""

    def __init__(self, db: Database):
        """Tworzy repozytorium oparte o podaną bazę"""
        self.db = db

    def add(self, r: Recipe) -> int:
        """Dodaje nowy przepis i zwraca jego ID."""
        with self.db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO recipes
                (
                    title,
                    ingredients,
                    instructions,
                    prep_time_minutes,
                    tags,
                    favorite,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    r.title,
                    r.ingredients,
                    r.instructions,
                    r.prep_time_minutes,
                    r.tags,
                    1 if r.favorite else 0,
                    r.created_at,
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def get(self, recipe_id: int) -> Optional[Recipe]:
        """Pobiera przepis po ID."""
        with self.db.connect() as conn:
            cur = conn.execute(
                "SELECT id, title, ingredients, instructions, "
                "prep_time_minutes, tags, favorite, "
                "created_at FROM recipes WHERE id = ?",
                (recipe_id,),
            )
            row = cur.fetchone()
            return self._row_to_recipe(row) if row else None

    def list_all(self) -> List[Recipe]:
        """Zwraca wszystkie przepisy, najnowsze pierwsze."""
        with self.db.connect() as conn:
            cur = conn.execute(
                "SELECT id, title, ingredients, "
                "instructions, prep_time_minutes, "
                "tags, favorite, created_at "
                "FROM recipes ORDER BY id DESC"
            )
            rows = cur.fetchall()
        return [self._row_to_recipe(r) for r in rows]

    def list_favorites(self) -> List[Recipe]:
        """Zwraca wszystkie przepisy oznaczone jako ulubione."""
        with self.db.connect() as conn:
            cur = conn.execute(
                "SELECT id, title, ingredients, "
                "instructions, prep_time_minutes, "
                "tags, favorite, created_at "
                "FROM recipes WHERE favorite = 1 ORDER BY id DESC"
            )
            rows = cur.fetchall()
        return [self._row_to_recipe(r) for r in rows]

    def set_favorite(self, recipe_id: int, fav: bool) -> None:
        """Ustawia/usuwa flagę ulubionego dla przepisu."""
        with self.db.connect() as conn:
            conn.execute(
                "UPDATE recipes SET favorite = ? WHERE id = ?",
                (1 if fav else 0, recipe_id),
            )
            conn.commit()

    def delete(self, recipe_id: int) -> None:
        """Usuwa przepis po ID."""
        with self.db.connect() as conn:
            conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            conn.commit()

    def update(self, r: Recipe) -> None:
        """Aktualizuje pełne dane przepisu."""
        if r.id is None:
            raise ValueError("Recipe must have id for update.")
        with self.db.connect() as conn:
            sql = (
                "UPDATE recipes SET "
                "title = ?, "
                "ingredients = ?, "
                "instructions = ?, "
                "prep_time_minutes = ?, "
                "tags = ?, "
                "favorite = ? "
                "WHERE id = ?"
            )
            params = (
                r.title,
                r.ingredients,
                r.instructions,
                r.prep_time_minutes,
                r.tags,
                1 if r.favorite else 0,
                r.id,
            )
            conn.execute(sql, params)
            conn.commit()

    def search(
        self,
        q: str = "",
        max_time: Optional[int] = None,
        only_fav: bool = False,
        tag: Optional[str] = None,
    ) -> list[Recipe]:
        """Wyszukuje przepisy wg tekstu, czasu, ulubionych i/lub tagu."""
        q = (q or "").strip()
        params = []
        clauses = []
        if q:
            like = f"%{q}%"
            clauses.append(
                "(title LIKE ? OR ingredients LIKE ? OR tags LIKE ?)"
            )
            params.extend([like, like, like])
        if max_time is not None:
            clauses.append(
                "(prep_time_minutes IS NOT NULL AND prep_time_minutes <= ?)"
            )
            params.append(int(max_time))
        if only_fav:
            clauses.append("favorite = 1")
        if tag:
            clauses.append("(tags LIKE ?)")
            params.append(f"%{tag}%")
        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = (
            "SELECT id, title, ingredients, instructions, "
            "prep_time_minutes, tags, favorite, created_at FROM recipes"
            + where
            + " ORDER BY id DESC"
        )
        with self.db.connect() as conn:
            cur = conn.execute(sql, params)
            rows = cur.fetchall()
        return [self._row_to_recipe(r) for r in rows]

    def count(self) -> int:
        """Zwraca liczbę wszystkich przepisów."""
        with self.db.connect() as conn:
            cur = conn.execute("SELECT COUNT(*) FROM recipes")
            return int(cur.fetchone()[0])

    def count_favorites(self) -> int:
        """Zwraca liczbę przepisów oznaczonych jako ulubione."""
        with self.db.connect() as conn:
            cur = conn.execute(
                "SELECT COUNT(*) FROM recipes WHERE favorite = 1"
            )
            return int(cur.fetchone()[0])

    def avg_prep_time(self) -> Optional[float]:
        """Zwraca średni czas przygotowania (minuty), jeśli istnieje."""
        with self.db.connect() as conn:
            cur = conn.execute(
                "SELECT AVG(prep_time_minutes) FROM recipes "
                "WHERE prep_time_minutes IS NOT NULL AND prep_time_minutes > 0"
            )
            val = cur.fetchone()[0]
            return float(val) if val is not None else None

    def list_tags(self) -> list[str]:
        """Zwraca posortowaną listę unikalnych tagów z bazy."""
        with self.db.connect() as conn:
            cur = conn.execute("SELECT tags FROM recipes")
            rows = cur.fetchall()
        tags = set()
        for (ts,) in rows:
            if not ts:
                continue
            for t in ts.split(","):
                t = t.strip()
                if t:
                    tags.add(t)
        return sorted(tags)

    @staticmethod
    def _row_to_recipe(row) -> Recipe:
        """Mapuje krotkę z bazy na obiekt `Recipe`."""
        return Recipe(
            id=row[0],
            title=row[1],
            ingredients=row[2],
            instructions=row[3],
            prep_time_minutes=row[4],
            tags=row[5],
            favorite=bool(row[6]),
            created_at=row[7],
        )
