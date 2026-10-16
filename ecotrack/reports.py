"""Summary generation for EcoTrack activity records."""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable

from .activities import Activity


@dataclass(frozen=True)
class FootprintSummary:
    """Aggregated emissions for a requested reporting period."""

    total_emissions: float
    highest_impact_category: str
    category_emissions: dict[str, float]
    activity_count: int
    period: str


def build_summary(
    activities: Iterable[Activity],
    period: str = "week",
    now: datetime | None = None,
) -> FootprintSummary:
    """Build an emissions summary for a requested time period.

    Supported periods:
        day: Activities since the beginning of the current local day.
        week: Activities from the last seven days.
        month: Activities from the last thirty days.
        all: Every activity supplied to this function.
    """
    if not isinstance(period, str):
        raise ValueError("period must be one of: day, week, month, all.")

    normalized_period = period.strip().lower()

    if normalized_period not in {"day", "week", "month", "all"}:
        raise ValueError("period must be one of: day, week, month, all.")

    current = now or datetime.now().astimezone()

    if normalized_period == "day":
        start = current.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
    elif normalized_period == "week":
        start = current - timedelta(days=7)
    elif normalized_period == "month":
        start = current - timedelta(days=30)
    else:
        start = None

    selected = []

    for activity in activities:
        if start is None:
            selected.append(activity)
            continue

        recorded_at = activity.recorded_at

        # Compare timestamps consistently when one value is timezone-aware
        # and the other is naive. Naive timestamps use the current local zone.
        if recorded_at.tzinfo is None and current.tzinfo is not None:
            recorded_at = recorded_at.replace(tzinfo=current.tzinfo)
        elif recorded_at.tzinfo is not None and current.tzinfo is None:
            current_for_comparison = current.replace(
                tzinfo=recorded_at.tzinfo
            )
            start = current_for_comparison - (
                timedelta(days=0)
                if normalized_period == "day"
                else timedelta(days=7)
                if normalized_period == "week"
                else timedelta(days=30)
            )
        else:
            current_for_comparison = current

        if normalized_period == "day":
            day_start = current_for_comparison.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
            if recorded_at >= day_start:
                selected.append(activity)
        elif start is not None and recorded_at >= start:
            selected.append(activity)

    totals: dict[str, float] = defaultdict(float)

    for activity in selected:
        totals[activity.category] += activity.emissions_kg_co2e

    total = sum(totals.values())
    highest = max(totals, key=totals.get) if totals else "None"

    return FootprintSummary(
        total_emissions=round(total, 2),
        highest_impact_category=highest,
        category_emissions={
            category: round(value, 2)
            for category, value in sorted(totals.items())
        },
        activity_count=len(selected),
        period=normalized_period,
    )