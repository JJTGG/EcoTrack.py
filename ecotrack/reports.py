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
        day: Activities from local midnight up to the current time.
        week: Activities from the last seven days up to the current time.
        month: Activities from the last thirty days up to the current time.
        all: Every activity supplied to this function.

    Naive timestamps are interpreted in the current local timezone.
    Future-dated activities are excluded from day, week, and month
    summaries.
    """
    if not isinstance(period, str):
        raise ValueError("period must be one of: day, week, month, all.")

    normalized_period = period.strip().lower()

    if normalized_period not in {"day", "week", "month", "all"}:
        raise ValueError("period must be one of: day, week, month, all.")

    current = now if now is not None else datetime.now().astimezone()

    # Normalize the reference time to an aware datetime. A naive
    # reference time is interpreted as local system time.
    if current.tzinfo is None or current.utcoffset() is None:
        current = current.astimezone()

    if normalized_period == "all":
        selected = list(activities)
    else:
        if normalized_period == "day":
            start = current.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        elif normalized_period == "week":
            start = current - timedelta(days=7)
        else:
            start = current - timedelta(days=30)

        selected = []

        for activity in activities:
            recorded_at = activity.recorded_at

            # Interpret naive activity timestamps in the reference
            # timezone. Convert aware timestamps to that same timezone.
            if (
                recorded_at.tzinfo is None
                or recorded_at.utcoffset() is None
            ):
                recorded_at = recorded_at.replace(
                    tzinfo=current.tzinfo
                )
            else:
                recorded_at = recorded_at.astimezone(current.tzinfo)

            if start <= recorded_at <= current:
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