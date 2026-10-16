"""Main activity-tracking interface for EcoTrack."""

from .activities import Activity
from .calculations import (
    calculate_diet_emissions,
    calculate_energy_emissions,
    calculate_transport_emissions,
)
from .reports import FootprintSummary, build_summary


class EcoTrack:
    """Track activities and estimate their carbon emissions.

    Activity records are kept in memory. They are not saved to disk or
    a database and will be lost when the Python process exits.
    """

    def __init__(self) -> None:
        """Initialize an empty activity tracker."""
        self._activities: list[Activity] = []

    def track_transport(
        self,
        mode: str,
        distance_km: float,
    ) -> Activity:
        """Record a transportation journey.

        Args:
            mode: Transportation mode, such as car, bus, or bicycle.
            distance_km: Journey distance in kilometres.

        Returns:
            The recorded activity.
        """
        emissions = calculate_transport_emissions(
            mode=mode,
            distance_km=distance_km,
        )

        normalized_mode = (
            mode.strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        activity = Activity(
            category="Transportation",
            details={
                "mode": normalized_mode,
                "distance_km": float(distance_km),
            },
            emissions_kg_co2e=emissions,
        )

        self._activities.append(activity)
        return activity

    def track_energy(
        self,
        source: str,
        consumption: float,
        unit: str = "kWh",
    ) -> Activity:
        """Record household energy consumption.

        Args:
            source: Energy source, such as electricity or natural gas.
            consumption: Amount of energy consumed.
            unit: Energy unit. Currently, only kWh is supported.

        Returns:
            The recorded activity.
        """
        emissions = calculate_energy_emissions(
            source=source,
            consumption=consumption,
            unit=unit,
        )

        normalized_source = (
            source.strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        activity = Activity(
            category="Energy Consumption",
            details={
                "source": normalized_source,
                "consumption": float(consumption),
                "unit": unit,
            },
            emissions_kg_co2e=emissions,
        )

        self._activities.append(activity)
        return activity

    def track_diet(
        self,
        food_type: str,
        servings: float,
    ) -> Activity:
        """Record a dietary choice.

        Args:
            food_type: Food category, such as beef, chicken, or vegan.
            servings: Number of servings.

        Returns:
            The recorded activity.
        """
        emissions = calculate_diet_emissions(
            food_type=food_type,
            servings=servings,
        )

        normalized_food = (
            food_type.strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        activity = Activity(
            category="Dietary Choices",
            details={
                "food_type": normalized_food,
                "servings": float(servings),
            },
            emissions_kg_co2e=emissions,
        )

        self._activities.append(activity)
        return activity

    def get_daily_footprint(self) -> float:
        """Return today's total estimated emissions in kg CO2e."""
        summary = build_summary(
            activities=self._activities,
            period="day",
        )

        return summary.total_emissions

    def get_activity_history(self) -> list[Activity]:
        """Return a copy of the recorded activity history."""
        return list(self._activities)

    def get_summary(
        self,
        period: str = "week",
    ) -> FootprintSummary:
        """Generate a summary for the requested reporting period.

        Supported periods are day, week, month, and all.
        """
        return build_summary(
            activities=self._activities,
            period=period,
        )