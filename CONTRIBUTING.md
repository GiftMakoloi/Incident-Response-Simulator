# Contributing Guidelines

Thank you for contributing to the Incident Response Simulator project.

## Adding New Incident Scenarios

1. Scenarios are defined using JSON structures containing steps, choices, impact metrics, and feedback.
2. To add a scenario, edit the scenario dictionary in `app.py` or submit a pull request modifying `scenarios.json`.
3. Ensure all decision branches resolve to a final review step.
