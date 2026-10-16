"""Data models for EcoTrack activities."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Activity:
    """Represent one recorded activity and its estimated emissions.

    Attributes:
        category: Activity category, such as Transportation.
        details: Activity-specific information, including units.
        emissions_kg_co2e: Estimated emissions in kilograms of CO2 equivalent.
        recorded_at: Date and time when the activity was recorded.
    """

    category: str
    details: dict[str, Any]
    emissions_kg_co2e: float
    recorded_at: datetime = field(
        default_factory=lambda: datetime.now().astimezone()
    )

    def as_dict(self) -> dict[str, Any]:
        """Return the activity as a JSON-friendly dictionary."""
        return {
            "category": self.category,
            **self.details,
            "emissions_kg_co2e": self.emissions_kg_co2e,
            "recorded_at": self.recorded_at.isoformat(),
        }