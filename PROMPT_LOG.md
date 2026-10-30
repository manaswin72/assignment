# PROMPT_LOG — AI Collaboration for Section 3

## Initial prompt

> Write a Python script that loads `device_summary.json` (a list of objects with `device_id` and `average_temperature`) and generates a matplotlib bar chart comparing average temperature per device. Save the figure as `avg_temperature_chart.png`. Include basic error handling if the JSON file is missing.

## Bug / formatting mistake in the first AI attempt

The first generated script drew the bars correctly, but:

1. It never called `plt.tight_layout()`, so the y-axis label and title were clipped when saved to PNG.
2. Device labels on the x-axis overlapped slightly on smaller figure sizes because no figure size was set and no padding was applied.
3. There was no chart title in the first draft (only axis labels).

## Follow-up prompt used to fix it

> Please fix the chart formatting: set an explicit figure size, add the title "Average Temperature by Device", call `tight_layout()` before saving, and add value labels above each bar so the PNG is readable and not clipped.

## What I kept after review

- File/JSON existence checks
- Explicit axes labels and title
- `tight_layout()` before `savefig`
- Value labels on bars for readability
