"""Section 2: Device Log Summarizer CLI.

Reads device telemetry CSV, aggregates per device, filters hot devices,
exports JSON, and prints a terminal summary table.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


TEMPERATURE_LIMIT = 80.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize device telemetry logs into JSON and a table."
    )
    parser.add_argument(
        "--input",
        default="device_telemetry.csv",
        help="Path to the telemetry CSV file (default: device_telemetry.csv)",
    )
    parser.add_argument(
        "--output",
        default="device_summary.json",
        help="Path for the JSON export (default: device_summary.json)",
    )
    return parser.parse_args()


def load_telemetry(csv_path: Path) -> list[dict[str, Any]]:
    """Load and lightly validate rows from the telemetry CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    required_columns = {"device_id", "status", "temperature"}
    rows: list[dict[str, Any]] = []

    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or missing a header row.")

        missing = required_columns - {name.strip() for name in reader.fieldnames}
        if missing:
            raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

        for line_number, raw_row in enumerate(reader, start=2):
            device_id = (raw_row.get("device_id") or "").strip()
            status = (raw_row.get("status") or "").strip().upper()
            temperature_raw = (raw_row.get("temperature") or "").strip()

            if not device_id or not temperature_raw:
                print(
                    f"Warning: skipping incomplete row at line {line_number}",
                    file=sys.stderr,
                )
                continue

            try:
                temperature = float(temperature_raw)
            except ValueError:
                print(
                    f"Warning: skipping non-numeric temperature at line {line_number}",
                    file=sys.stderr,
                )
                continue

            rows.append(
                {
                    "device_id": device_id,
                    "status": status,
                    "temperature": temperature,
                }
            )

    return rows


def aggregate_by_device(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group rows by device_id and compute count / mean temp / ERROR count."""
    totals: dict[str, int] = defaultdict(int)
    temp_sums: dict[str, float] = defaultdict(float)
    error_counts: dict[str, int] = defaultdict(int)

    for row in rows:
        device_id = row["device_id"]
        totals[device_id] += 1
        temp_sums[device_id] += row["temperature"]
        if row["status"] == "ERROR":
            error_counts[device_id] += 1

    summaries: list[dict[str, Any]] = []
    for device_id in sorted(totals):
        count = totals[device_id]
        average_temperature = round(temp_sums[device_id] / count, 2)
        summaries.append(
            {
                "device_id": device_id,
                "record_count": count,
                "average_temperature": average_temperature,
                "error_count": error_counts[device_id],
            }
        )

    return summaries


def filter_hot_devices(
    summaries: list[dict[str, Any]], limit: float = TEMPERATURE_LIMIT
) -> list[dict[str, Any]]:
    """Keep devices whose average temperature is at or below the limit."""
    return [item for item in summaries if item["average_temperature"] <= limit]


def export_json(summaries: list[dict[str, Any]], output_path: Path) -> None:
    output_path.write_text(
        json.dumps(summaries, indent=2) + "\n",
        encoding="utf-8",
    )


def print_summary_table(summaries: list[dict[str, Any]]) -> None:
    if not summaries:
        print("No devices remaining after filtering.")
        return

    headers = ("device_id", "record_count", "average_temperature", "error_count")
    widths = {
        "device_id": max(len(headers[0]), *(len(item["device_id"]) for item in summaries)),
        "record_count": len(headers[1]),
        "average_temperature": len(headers[2]),
        "error_count": len(headers[3]),
    }

    def format_row(values: dict[str, Any]) -> str:
        return (
            f"{str(values['device_id']):<{widths['device_id']}}  "
            f"{str(values['record_count']):>{widths['record_count']}}  "
            f"{str(values['average_temperature']):>{widths['average_temperature']}}  "
            f"{str(values['error_count']):>{widths['error_count']}}"
        )

    header_row = format_row(
        {
            "device_id": headers[0],
            "record_count": headers[1],
            "average_temperature": headers[2],
            "error_count": headers[3],
        }
    )
    print(header_row)
    print("-" * len(header_row))
    for item in summaries:
        print(format_row(item))


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        rows = load_telemetry(input_path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not rows:
        print("Error: no valid telemetry rows found.", file=sys.stderr)
        return 1

    aggregated = aggregate_by_device(rows)
    filtered = filter_hot_devices(aggregated)

    export_json(filtered, output_path)
    print(f"Wrote {len(filtered)} device summaries to {output_path}")
    print()
    print_summary_table(filtered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
