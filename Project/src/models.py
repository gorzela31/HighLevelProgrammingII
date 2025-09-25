"""Domain models for Przepisnik."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Recipe:
    """Represents a cooking recipe."""

    id: Optional[int]
    title: str
    ingredients: str
    instructions: str
    prep_time_minutes: int = 0
    tags: str = ""
    favorite: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        )
    )

    @staticmethod
    def new(
        title: str,
        ingredients: str,
        instructions: str,
        prep_time_minutes: int = 0,
        tags: str = "",
        favorite: bool = False,
    ) -> "Recipe":
        """Factory with simple validation."""
        title = (title or "").strip()
        if not title:
            raise ValueError("Tytuł jest wymagany.")
        if prep_time_minutes < 0:
            raise ValueError("Czas przygotowania nie może być ujemny.")
        return Recipe(
            id=None,
            title=title,
            ingredients=(ingredients or "").strip(),
            instructions=(instructions or "").strip(),
            prep_time_minutes=int(prep_time_minutes),
            tags=(tags or "").strip(),
            favorite=bool(favorite),
        )
