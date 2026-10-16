"""Carbon-emission calculations for EcoTrack.

The default emission factors are illustrative starter values, not an
authoritative dataset. Replace them with documented, location-appropriate
factors before using estimates for formal reporting or decision-making.
"""

import math
from collections.abc import Mapping


# Illustrative transportation factors:
# kg CO2e per kilometre.
TRANSPORT_EMISSION_FACTORS: dict[str, float] = {
    "car": 0.192,
    "bus": 0.105,
    "public_transport": 0.105,
    "train": 0.041,
    "motorcycle": 0.103,
    "bicycle": 0.0,
    "walking": 0.0,
}

# Illustrative energy factors:
# kg CO2e per kWh.
ENERGY_EMISSION_FACTORS: dict[str, float] = {
    "electricity": 0.400,
    "natural_gas": 0.202,
    "gas": 0.202,
    "solar": 0.0,
}

# Illustrative dietary factors:
# kg CO2e per serving.
DIET_EMISSION_FACTORS: dict[str, float] = {
    "beef": 5.0,
    "lamb": 4.5,
    "pork": 1.7,
    "chicken": 1.1,
    "fish": 1.5,
    "dairy": 0.8,
    "vegetarian": 0.7,
    "vegan": 0.5,
    "plant_based": 0.5,
}


def _non_negative_number(value: float, name: str) -> float:
    """Convert a value to a finite, non-negative float."""
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a non-negative number.")

    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{name} must be a non-negative number."
        ) from exc

    if not math.isfinite(number) or number < 0:
        raise ValueError(
            f"{name} must be a finite, non-negative number."
        )

    return number


def _normalise(value: str, name: str) -> str:
    """Normalize a category name for lookup."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string.")

    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _emissions(
    key: str,
    quantity: float,
    factors: Mapping[str, float],
    factor_name: str,
) -> float:
    """Calculate emissions using a factor measured in compatible units."""
    if key not in factors:
        supported = ", ".join(sorted(factors))
        raise ValueError(
            f"Unsupported {factor_name} {key!r}. "
            f"Supported values: {supported}."
        )

    factor = _non_negative_number(
        factors[key],
        f"Emission factor for {key}",
    )

    return round(quantity * factor, 4)


def calculate_transport_emissions(
    mode: str,
    distance_km: float,
    factors: Mapping[str, float] | None = None,
) -> float:
    """Estimate transport emissions in kg CO2e for a distance in kilometres."""
    normalized_mode = _normalise(mode, "mode")
    distance = _non_negative_number(distance_km, "distance_km")
    emission_factors = (
        TRANSPORT_EMISSION_FACTORS if factors is None else factors
    )

    return _emissions(
        normalized_mode,
        distance,
        emission_factors,
        "transport mode",
    )


def calculate_energy_emissions(
    source: str,
    consumption: float,
    unit: str = "kWh",
    factors: Mapping[str, float] | None = None,
) -> float:
    """Estimate energy emissions in kg CO2e.

    This version accepts consumption measured in kilowatt-hours only.
    """
    if not isinstance(unit, str) or unit.strip().lower() != "kwh":
        raise ValueError("unit must be 'kWh' in this version.")

    normalized_source = _normalise(source, "source")
    amount = _non_negative_number(consumption, "consumption")
    emission_factors = (
        ENERGY_EMISSION_FACTORS if factors is None else factors
    )

    return _emissions(
        normalized_source,
        amount,
        emission_factors,
        "energy source",
    )


def calculate_diet_emissions(
    food_type: str,
    servings: float,
    factors: Mapping[str, float] | None = None,
) -> float:
    """Estimate dietary emissions in kg CO2e for a number of servings."""
    normalized_food = _normalise(food_type, "food_type")
    amount = _non_negative_number(servings, "servings")
    emission_factors = (
        DIET_EMISSION_FACTORS if factors is None else factors
    )

    return _emissions(
        normalized_food,
        amount,
        emission_factors,
        "food type",
    )