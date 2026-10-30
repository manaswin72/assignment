# Device Log Summarizer

Software Engineering Intern coding assessment — a small CLI pipeline that cleans sensor values, summarizes device telemetry, and charts average temperatures.

## Project layout

| File | Section | Purpose |
|------|---------|---------|
| `clean_sensors.py` | 1 | Clean/normalize mixed sensor readings + tests |
| `device_telemetry.csv` | 2 | Sample telemetry input |
| `summarize_logs.py` | 2 | Aggregate CSV → filter → JSON + table |
| `device_summary.json` | 2 | Sample output (generated) |
| `chart_temps.py` | 3 | Bar chart from JSON (matplotlib) |
| `avg_temperature_chart.png` | 3 | Sample chart image (generated) |
| `PROMPT_LOG.md` | 3 | How AI was used for charting |
| `INTERVIEW_PREP.md` | — | Talking points for the follow-up interview |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Section 1–2 need only the Python standard library. Matplotlib is required for Section 3.

## Run

```bash
# Section 1 — cleaning function + tests
python3 clean_sensors.py

# Section 2 — summarize telemetry
python3 summarize_logs.py --input device_telemetry.csv --output device_summary.json

# Section 3 — chart average temperatures
python3 chart_temps.py --input device_summary.json --output avg_temperature_chart.png
```

## Behavior notes

- Devices with **average temperature > 80.0** are filtered out of the JSON/table/chart.
- Missing CSV/JSON, bad rows, and empty inputs are handled with clear errors or skip warnings instead of unhandled crashes.
