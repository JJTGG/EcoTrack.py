# Contributing to EcoTrack

Thank you for your interest in contributing to EcoTrack!

EcoTrack is an open-source Python project designed to help people understand
their personal carbon footprint by tracking transportation, household energy
consumption, and dietary activities.

We welcome bug reports, feature proposals, code improvements, documentation
updates, and new tests.

## Getting Started

Before contributing, familiarize yourself with the existing project structure:

```text
ecotrack/
├── ecotrack/
│   ├── __init__.py
│   ├── activities.py
│   ├── calculations.py
│   ├── reports.py
│   └── tracker.py
├── tests/
├── docs/
├── pyproject.toml
├── requirements-dev.txt
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

The principal modules have distinct responsibilities:

- `activities.py` defines the activity data model.
- `calculations.py` contains emission factors and calculation functions.
- `reports.py` aggregates activity records into summaries.
- `tracker.py` provides the main `EcoTrack` interface.
- `tests/` contains automated tests.
- `docs/` contains technical documentation.

## Reporting Bugs

When reporting a bug, include:

1. A clear description of the problem.
2. The expected behavior.
3. The actual behavior.
4. A minimal example that reproduces the problem.
5. Any relevant error messages.

Do not include passwords, API keys, private information, or other secrets.

## Proposing Features

For substantial changes, open a GitHub issue before starting implementation.

Explain the problem being addressed, the proposed solution, and any changes
to the public API.

Potential improvements include persistent activity storage, configurable
emission factors, additional activity categories, historical reporting, and
data export.

## Code Guidelines

Please follow these principles:

- Write readable, maintainable Python code.
- Use descriptive function, variable, and class names.
- Add docstrings to public classes and functions.
- Use type annotations for public APIs where practical.
- Validate user inputs and handle invalid values explicitly.
- Keep modules focused on their intended responsibilities.
- Avoid adding dependencies without a clear reason.
- Preserve compatibility with Python 3.10 and later unless a change is
  explicitly discussed and documented.

## Testing

EcoTrack uses `pytest` for automated tests.

Add tests for new features and bug fixes. For calculation changes, verify
normal results, boundary conditions, invalid inputs, and any relevant
unit conversions.

The repository's GitHub Actions workflow should run the test suite whenever
changes are pushed or a pull request is opened.

A contribution is not considered verified merely because the code has been
committed. Review the completed workflow and address any failures.

## Emission Factors and Scientific Accuracy

Carbon footprint estimates depend on the emission factors and assumptions
used by the application.

When proposing or changing emission factors:

- Identify the original data source.
- Document the publication date and geographical scope where available.
- Specify the factor's units.
- Explain the system boundaries and calculation assumptions.
- Consider uncertainty and known limitations.
- Add or update tests for the resulting calculations.
- Avoid describing illustrative values as authoritative or scientifically
  validated.

Consult `docs/emission-factors.md` for the current implementation's
limitations and documentation requirements.

## Submitting Changes

1. Check existing issues to avoid duplicating work.
2. Make a focused change addressing one problem or feature.
3. Add or update tests and documentation.
4. Review the changes for correctness and unintended behavior.
5. Commit with a descriptive message.
6. Open a pull request describing the change, its motivation, and how it
   was tested.

Keep pull requests focused and provide enough context for another developer
to review the changes.

## Documentation

Update relevant documentation when changing public APIs, supported activity
categories, calculation behavior, configuration, or known limitations.

Documentation must describe implemented behavior accurately. Proposed
features should not be presented as completed functionality.

## Code of Conduct

Be respectful, constructive, and considerate of other contributors.

Welcome good-faith questions, provide helpful feedback, and focus technical
disagreements on evidence and implementation rather than individuals.

## License

By contributing to EcoTrack, you agree that your contributions will be
distributed under the project's MIT License.