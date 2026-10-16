"""Tests for EcoTrack's activity data model."""

import json
from datetime import datetime, timezone

from ecotrack.activities import Activity


def test_activity_as_dict_contains_expected_fields():
    recorded_at = datetime(
        2026,
        10,
        16,
        12,
        30,
        tzinfo=timezone.utc,
    )

    activity = Activity(
        category="Transportation",
        details={
            "mode": "car",
            "distance_km": 5.0,
        },
        emissions_kg_co2e=0.96,
        recorded_at=recorded_at,
    )

    result = activity.as_dict()

    assert result == {
        "category": "Transportation",
        "mode": "car",
        "distance_km": 5.0,
        "emissions_kg_co2e": 0.96,
        "recorded_at": "2026-10-16T12:30:00+00:00",
    }


def test_activity_as_dict_is_json_serializable():
    activity = Activity(
        category="Energy Consumption",
        details={
            "source": "electricity",
            "consumption": 8.0,
            "unit": "kWh",
        },
        emissions_kg_co2e=3.2,
        recorded_at=datetime(
            2026,
            10,
            16,
            12,
            30,
            tzinfo=timezone.utc,
        ),
    )

    serialized = json.dumps(activity.as_dict())
    restored = json.loads(serialized)

    assert restored["category"] == "Energy Consumption"
    assert restored["consumption"] == 8.0
    assert restored["emissions_kg_co2e"] == 3.2
    assert restored["recorded_at"] == "2026-10-16T12:30:00+00:00"


def test_default_activity_timestamp_is_timezone_aware():
    activity = Activity(
        category="Dietary Choices",
        details={
            "food_type": "vegan",
            "servings": 1.0,
        },
        emissions_kg_co2e=0.5,
    )

    assert activity.recorded_at.tzinfo is not None
    assert activity.recorded_at.utcoffset() is not None