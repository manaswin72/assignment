"""Section 3: Load device summary JSON and plot average temperature bars."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot average temperature per device from summary JSON."
    )
    parser.add_argument(
        "--input",
        default="device_summary.json",
        help="Path to the JSON summary from summarize_logs.py",
    )
    parser.add_argument(
        "--output",
        default="avg_temperature_chart.png",
        help="Path for the saved chart image",
    )
    return parser.parse_args()


def load_summaries(json_path: Path) -> list[dict]:
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    data = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Expected a JSON list of device summaries.")
    return data


def create_chart(summaries: list[dict], output_path: Path) -> None:
    if not summaries:
        raise ValueError("No device summaries available to chart.")

    devices = [item["device_id"] for item in summaries]
    averages = [item["average_temperature"] for item in summaries]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(devices, averages, color="#2F6F8F", edgecolor="white")

    ax.set_title("Average Temperature by Device", fontsize=14, pad=12)
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature (°C)")
    ax.set_ylim(0, max(averages) * 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    for bar, value in zip(bars, averages):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{value:.1f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        summaries = load_summaries(input_path)
        create_chart(summaries, output_path)
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved chart to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
