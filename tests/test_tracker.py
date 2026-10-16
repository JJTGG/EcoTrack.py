"""Tests for EcoTrack's activity-tracking interface."""

import pytest

from ecotrack import EcoTrack


def test_tracker_records_transportation():
    tracker = EcoTrack()

    activity = tracker.track_transport(
        mode="car",
        distance_km=15,
    )

    assert activity.category == "Transportation"
    assert activity.details["mode"] == "car"
    assert activity.details["distance_km"] == 15.0
    assert activity.emissions_kg_co2e == pytest.approx(2.88)


def test_tracker_records_energy():
    tracker = EcoTrack()

    activity = tracker.track_energy(
        source="electricity",
        consumption=8,
        unit="kWh",
    )

    assert activity.category == "Energy Consumption"
    assert activity.details["source"] == "electricity"
    assert activity.details["consumption"] == 8.0
    assert activity.emissions_kg_co2e == pytest.approx(3.2)


def test_tracker_records_diet():
    tracker = EcoTrack()

    activity = tracker.track_diet(
        food_type="beef",
        servings=1,
    )

    assert activity.category == "Dietary Choices"
    assert activity.details["food_type"] == "beef"
    assert activity.details["servings"] == 1.0
    assert activity.emissions_kg_co2e == pytest.approx(5.0)


def test_tracker_records_multiple_activities():
    tracker = EcoTrack()

    tracker.track_transport(mode="car", distance_km=15)
    tracker.track_energy(
        source="electricity",
        consumption=8,
        unit="kWh",
    )
    tracker.track_diet(food_type="beef", servings=1)

    history = tracker.get_activity_history()

    assert len(history) == 3
    assert [activity.category for activity in history] == [
        "Transportation",
        "Energy Consumption",
        "Dietary Choices",
    ]


def test_daily_footprint_calculates_total():
    tracker = EcoTrack()

    tracker.track_transport(mode="car", distance_km=15)
    tracker.track_energy(
        source="electricity",
        consumption=8,
        unit="kWh",
    )
    tracker.track_diet(food_type="beef", servings=1)

    assert tracker.get_daily_footprint() == pytest.approx(11.08)


def test_weekly_summary_calculates_category_totals():
    tracker = EcoTrack()

    tracker.track_transport(mode="car", distance_km=15)
    tracker.track_energy(
        source="electricity",
        consumption=8,
        unit="kWh",
    )
    tracker.track_diet(food_type="beef", servings=1)

    summary = tracker.get_summary(period="week")

    assert summary.total_emissions == pytest.approx(11.08)
    assert summary.highest_impact_category == "Dietary Choices"
    assert summary.activity_count == 3

    assert summary.category_emissions == {
        "Dietary Choices": 5.0,
        "Energy Consumption": 3.2,
        "Transportation": 2.88,
    }


def test_all_time_summary_includes_all_recorded_activities():
    tracker = EcoTrack()

    tracker.track_transport(mode="bus", distance_km=10)
    tracker.track_diet(food_type="vegan", servings=2)

    summary = tracker.get_summary(period="all")

    assert summary.period == "all"
    assert summary.activity_count == 2
    assert summary.total_emissions == pytest.approx(2.05)


def test_empty_tracker_returns_zero_footprint():
    tracker = EcoTrack()

    assert tracker.get_daily_footprint() == 0.0

    summary = tracker.get_summary(period="week")

    assert summary.total_emissions == 0.0
    assert summary.highest_impact_category == "None"
    assert summary.activity_count == 0
    assert summary.category_emissions == {}


def test_history_returns_a_separate_list():
    tracker = EcoTrack()

    tracker.track_transport(mode="car", distance_km=5)

    history = tracker.get_activity_history()
    history.clear()

    assert len(tracker.get_activity_history()) == 1


def test_invalid_activity_is_not_recorded():
    tracker = EcoTrack()

    with pytest.raises(ValueError):
        tracker.track_transport(
            mode="spaceship",
            distance_km=10,
        )

    assert tracker.get_activity_history() == []


@pytest.mark.parametrize(
    "period",
    ["quarter", "year", "", None],
)
def test_invalid_summary_period_is_rejected(period):
    tracker = EcoTrack()

    with pytest.raises(ValueError):
        tracker.get_summary(period=period)