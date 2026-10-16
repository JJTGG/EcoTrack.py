# Changelog

All notable changes to EcoTrack are documented in this file.

The project uses version numbers following Semantic Versioning where
practical.

## [Unreleased]

### Added

- Automated tests for transportation, energy, and dietary calculations.
- Activity tracking and reporting tests.
- Regression tests for reporting time windows and timezone handling.
- GitHub Actions testing across Python 3.10, 3.11, 3.12, and 3.13.
- Documentation explaining the limitations of the starter emission factors.
- Contribution guidelines for developers.

### Changed

- Daily, weekly, and monthly summaries exclude future-dated activities.
- Reporting handles timezone-naive activity timestamps consistently.

### Notes

- Emission factors are illustrative starter values, not an authoritative
  scientific dataset.
- Activity records are kept in memory and are not persisted after the
  Python process exits.
- Energy consumption currently supports kWh only.