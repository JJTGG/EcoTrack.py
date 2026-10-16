# Emission Factor Documentation

## Purpose

EcoTrack estimates carbon emissions associated with transportation, household
energy consumption, and dietary activities.

The calculation engine uses emission factors to convert recorded activity
quantities into estimated kilograms of carbon dioxide equivalent (kg CO2e).

This document explains the units and limitations of the default factors.

## Current Calculation Categories

### Transportation

Transportation factors represent estimated emissions per kilometre travelled.

| Mode | Default factor | Unit |
|---|---:|---|
| Car | 0.192 | kg CO2e/km |
| Bus | 0.105 | kg CO2e/km |
| Public transport | 0.105 | kg CO2e/km |
| Train | 0.041 | kg CO2e/km |
| Motorcycle | 0.103 | kg CO2e/km |
| Bicycle | 0.000 | kg CO2e/km |
| Walking | 0.000 | kg CO2e/km |

The current implementation does not distinguish between vehicle models,
fuel types, occupancy levels, or geographical locations.

### Household Energy

Energy factors represent estimated emissions per kilowatt-hour consumed.

| Energy source | Default factor | Unit |
|---|---:|---|
| Electricity | 0.400 | kg CO2e/kWh |
| Natural gas | 0.202 | kg CO2e/kWh |
| Gas | 0.202 | kg CO2e/kWh |
| Solar | 0.000 | kg CO2e/kWh |

The electricity factor does not account for regional electricity-grid
differences. The energy model also does not yet distinguish between all
possible fuel types or energy-system boundaries.

The implementation accepts energy quantities in kWh only.

### Dietary Activities

Dietary factors represent illustrative emissions per serving.

| Food category | Default factor | Unit |
|---|---:|---|
| Beef | 5.000 | kg CO2e/serving |
| Lamb | 4.500 | kg CO2e/serving |
| Pork | 1.700 | kg CO2e/serving |
| Chicken | 1.100 | kg CO2e/serving |
| Fish | 1.500 | kg CO2e/serving |
| Dairy | 0.800 | kg CO2e/serving |
| Vegetarian | 0.700 | kg CO2e/serving |
| Vegan | 0.500 | kg CO2e/serving |
| Plant-based | 0.500 | kg CO2e/serving |

A serving does not currently have a standardized mass or portion size.
Different ingredients, production systems, and preparation methods can
produce substantially different emissions.

## How Calculations Work

EcoTrack multiplies the recorded activity quantity by its selected emission
factor.

For example, the default car calculation is:

    15 km × 0.192 kg CO2e/km = 2.88 kg CO2e

The default electricity calculation is:

    8 kWh × 0.400 kg CO2e/kWh = 3.20 kg CO2e

These examples demonstrate the software's arithmetic. They do not establish
the scientific accuracy of the factor values.

## Limitations

The current default factors are illustrative development values. They are
not a verified dataset, official carbon-accounting methodology, or
location-specific measurement.

Results can vary with:

- Geographical location and electricity-grid composition.
- Vehicle type, fuel, occupancy, and distance-measurement assumptions.
- Energy source and the system boundaries used by a dataset.
- Food ingredients, production methods, serving sizes, and supply chains.
- Whether an estimate includes direct emissions alone or broader lifecycle
  emissions.

EcoTrack must not present these starter values as precise measurements or
verified environmental claims.

## Future Improvements

Before using EcoTrack for substantive environmental comparisons, the project
should:

1. Identify authoritative, traceable sources for each emission factor.
2. Record the source, publication date, geographical scope, and units.
3. Define consistent lifecycle and system-boundary assumptions.
4. Support configurable regional factors and appropriate conversion rules.
5. Add tests that verify calculations, units, and factor selection.
6. Document uncertainty and known limitations in generated reports.

Custom emission factors are accepted by the calculation functions, allowing
developers to supply alternative mappings when they have suitable data.

## Source Transparency

No authoritative external dataset is currently assigned to the default
values in `ecotrack/calculations.py`.

Contributors must not label these defaults as sourced or scientifically
validated until their provenance has been established and documented.

When authoritative sources are adopted, list them here along with the
specific factors derived from each source.