"""Tests for EcoTrack's carbon-emission calculations."""

import pytest

from ecotrack.calculations import (
    calculate_diet_emissions,
    calculate_energy_emissions,
    calculate_transport_emissions,
)


def test_transport_emissions_for_car_trip():
    result = calculate_transport_emissions(
        mode="car",
        distance_km=15,
    )

    assert result == pytest.approx(2.88)


def test_transport_mode_is_normalized():
    result = calculate_transport_emissions(
        mode=" Public Transport ",
        distance_km=10,
    )

    assert result == pytest.approx(1.05)


def test_bicycle_has_zero_emissions_with_default_factor():
    result = calculate_transport_emissions(
        mode="bicycle",
        distance_km=20,
    )

    assert result == 0.0


def test_energy_emissions_for_electricity():
    result = calculate_energy_emissions(
        source="electricity",
        consumption=8,
        unit="kWh",
    )

    assert result == pytest.approx(3.2)


def test_energy_source_is_normalized():
    result = calculate_energy_emissions(
        source=" Natural Gas ",
        consumption=10,
    )

    assert result == pytest.approx(2.02)


def test_energy_rejects_unsupported_units():
    with pytest.raises(ValueError, match="unit must be 'kWh'"):
        calculate_energy_emissions(
            source="electricity",
            consumption=8,
            unit="MJ",
        )


def test_diet_emissions_for_beef():
    result = calculate_diet_emissions(
        food_type="beef",
        servings=1,
    )

    assert result == pytest.approx(5.0)


def test_diet_category_is_normalized():
    result = calculate_diet_emissions(
        food_type="plant-based",
        servings=2,
    )

    assert result == pytest.approx(1.0)


@pytest.mark.parametrize(
    "distance",
    [-1, float("nan"), float("inf"), float("-inf")],
)
def test_transport_rejects_invalid_distance(distance):
    with pytest.raises(ValueError):
        calculate_transport_emissions(
            mode="car",
            distance_km=distance,
        )


@pytest.mark.parametrize(
    "consumption",
    [-1, float("nan"), float("inf")],
)
def test_energy_rejects_invalid_consumption(consumption):
    with pytest.raises(ValueError):
        calculate_energy_emissions(
            source="electricity",
            consumption=consumption,
        )


@pytest.mark.parametrize(
    "servings",
    [-1, float("nan"), float("inf")],
)
def test_diet_rejects_invalid_servings(servings):
    with pytest.raises(ValueError):
        calculate_diet_emissions(
            food_type="beef",
            servings=servings,
        )


def test_transport_rejects_unknown_mode():
    with pytest.raises(ValueError, match="Unsupported transport mode"):
        calculate_transport_emissions(
            mode="spaceship",
            distance_km=10,
        )


def test_energy_rejects_unknown_source():
    with pytest.raises(ValueError, match="Unsupported energy source"):
        calculate_energy_emissions(
            source="unknown_fuel",
            consumption=10,
        )


def test_diet_rejects_unknown_food_type():
    with pytest.raises(ValueError, match="Unsupported food type"):
        calculate_diet_emissions(
            food_type="unknown_food",
            servings=1,
        )


def test_custom_transport_factor_can_be_supplied():
    result = calculate_transport_emissions(
        mode="car",
        distance_km=10,
        factors={"car": 0.25},
    )

    assert result == pytest.approx(2.5)