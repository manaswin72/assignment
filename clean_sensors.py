"""Section 1: Clean and normalize mixed sensor readings."""

from __future__ import annotations

from typing import Any


def clean_sensor_readings(raw_values: list[Any]) -> list[float]:
    """Convert mixed sensor inputs into cleaned, clipped floats.

    Rules:
    1. Convert to float where possible; drop None, non-numeric, and negative values.
    2. Cap any value above 500.0 at 500.0.
    3. Empty / all-invalid input returns [] without raising.
    """
    cleaned: list[float] = []

    if not raw_values:
        return cleaned

    for value in raw_values:
        if value is None:
            continue

        try:
            number = float(value)
        except (TypeError, ValueError):
            continue

        if number < 0:
            continue

        if number > 500.0:
            number = 500.0

        cleaned.append(number)

    return cleaned


def _run_tests() -> None:
    # Mixed valid/invalid values, including clipping.
    assert clean_sensor_readings(
        [10, "20.5", None, -3, "bad", 600, "100"]
    ) == [10.0, 20.5, 500.0, 100.0]

    # Empty list and all-invalid list should not raise.
    assert clean_sensor_readings([]) == []
    assert clean_sensor_readings([None, "x", -1, object()]) == []

    # Boundary: exactly 0 stays; exactly 500 stays.
    assert clean_sensor_readings([0, 500, "0.0"]) == [0.0, 500.0, 0.0]

    print("All clean_sensor_readings tests passed.")


if __name__ == "__main__":
    _run_tests()
