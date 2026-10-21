# Device Log Summarizer CLI Tool

A command-line tool that processes device telemetry data from CSV files, computes per-device statistics, and generates visual reports.

Built as part of a Software Engineering Intern technical assessment.

## Prerequisites

- Python 3.8 or higher
- matplotlib (for chart generation)

```
pip install matplotlib
```

Sections 1 and 2 only use Python standard library so matplotlib is only needed for Section 3.

## Project Files

| File | Description |
|------|-------------|
| `sanitizer.py` | Section 1 - Function to clean and normalize sensor readings with test cases |
| `test_sanitizer.py` | Section 1 - Unit tests using the unittest framework |
| `device_telemetry.csv` | Section 2 - Sample input CSV with device telemetry records |
| `summarizer.py` | Section 2 - Main CLI tool for data ingestion, grouping, filtering and export |
| `summary_output.json` | Section 2 - Generated JSON output file |
| `visualize.py` | Section 3 - Bar chart generator using matplotlib |
| `device_temperatures.png` | Section 3 - Generated chart image |
| `PROMPT_LOG.md` | Section 3 - AI interaction log documenting prompts and bug fixes |

## How to Run

### Section 1: Sensor Reading Sanitizer 

The sanitizer function handles cleaning raw sensor data - converts to float, drops None/negative/unconvertible values, and caps anything above 500.

Run the function with built-in test cases:
```
python sanitizer.py
```

Run the full unit test suite:
```
python -m unittest test_sanitizer.py
```

### Section 2: Device Log Summarizer 

The main CLI tool reads device_telemetry.csv, groups records by device_id, computes statistics (total records, average temperature, min/max, error count), filters out devices averaging above 80°C, and exports the results.

Run with default input file:
```
python summarizer.py
```

Run with a custom CSV file:
```
python summarizer.py path/to/your/data.csv
```

Output:
- Prints a formatted summary table to the terminal
- Saves filtered results to `summary_output.json`

### Section 3: Temperature Visualization 

Generates a color-coded bar chart from the JSON output showing average temperature per device with labels, a threshold line, and a legend.

```
python visualize.py
```

This creates `device_temperatures.png` in the current directory.

See `PROMPT_LOG.md` for documentation of the AI prompts used and bugs that were fixed.
