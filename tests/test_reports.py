"""Tests for EcoTrack reporting and time-window behavior."""

from datetime import datetime, timedelta, timezone

from ecotrack.activities import Activity
from ecotrack.reports import build_summary


def make_activity(recorded_at: datetime, emissions: float = 1.0) -> Activity:
    """Create an activity with a controlled timestamp for testing."""
    return Activity(
        category="Transportation",
        details={"mode": "car", "distance_km": 5.0},
        emissions_kg_co2e=emissions,
        recorded_at=recorded_at,
    )


def test_day_summary_accepts_naive_timestamp_with_aware_now():
    now = datetime(2026, 10, 16, 12, 0, tzinfo=timezone.utc)
    activity = make_activity(datetime(2026, 10, 16, 9, 0), emissions=2.5)

    summary = build_summary([activity], period="day", now=now)

    assert summary.total_emissions == 2.5
    assert summary.activity_count == 1


def test_rolling_summary_excludes_future_activities():
    now = datetime(2026, 10, 16, 12, 0, tzinfo=timezone.utc)
    future_activity = make_activity(
        now + timedelta(hours=1),
        emissions=3.0,
    )

    summary = build_summary(
        [future_activity],
        period="week",
        now=now,
    )

    assert summary.total_emissions == 0.0
    assert summary.activity_count == 0


def test_day_summary_uses_the_current_timezone_day_boundary():
    local_timezone = timezone(timedelta(hours=2))
    now = datetime(2026, 10, 16, 0, 30, tzinfo=local_timezone)

    previous_local_day = make_activity(
        datetime(2026, 10, 15, 21, 30, tzinfo=timezone.utc),
        emissions=4.0,
    )
    current_local_day = make_activity(
        datetime(2026, 10, 15, 22, 15, tzinfo=timezone.utc),
        emissions=2.0,
    )

    summary = build_summary(
        [previous_local_day, current_local_day],
        period="day",
        now=now,
    )

    assert summary.total_emissions == 2.0
    assert summary.activity_count == 1