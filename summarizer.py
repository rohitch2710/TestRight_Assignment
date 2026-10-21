import csv
import json
import sys
import os

VERBOSE = False  

def log(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


def read_csv_file(filepath):
    if not os.path.exists(filepath):
        print(f"\nError: Could not find '{filepath}'")
        print("Make sure device_telemetry.csv is in the same directory as this script.")
        print("You can also pass a custom path: python summarizer.py <path_to_csv>")
        sys.exit(1)

    records = []
    skipped_rows = 0
    total_lines = 0

    try:
        with open(filepath, "r", newline="") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("Error: CSV file appears to be empty.")
                sys.exit(1)

            headers = [h.strip() for h in reader.fieldnames]
            required = ["device_id", "status", "temperature"]

            missing = []
            for col in required:
                if col not in headers:
                    missing.append(col)

            if len(missing) > 0:
                print(f"Error: CSV is missing columns: {missing}")
                print(f"Found columns: {headers}")
                print(f"Required columns: {required}")
                sys.exit(1)

            for row in reader:
                total_lines += 1

                device_id = row.get("device_id", "")
                status = row.get("status", "")
                temp_raw = row.get("temperature", "")

                if device_id is None or device_id.strip() == "":
                    skipped_rows += 1
                    continue

                device_id = device_id.strip()
                status = status.strip() if status else ""

                if temp_raw is None or temp_raw.strip() == "":
                    skipped_rows += 1
                    continue

                try:
                    temperature = float(temp_raw.strip())
                except ValueError:
                    print(f"  Warning: Could not parse temperature '{temp_raw}' for device {device_id}, skipping row")
                    skipped_rows += 1
                    continue

                records.append({
                    "device_id": device_id,
                    "status": status,
                    "temperature": temperature
                })

    except PermissionError:
        print(f"Error: Permission denied when trying to read '{filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Something went wrong reading the CSV: {e}")
        sys.exit(1)

    log(f"  Parsed {total_lines} rows from CSV")
    log(f"  Valid records: {len(records)}")
    if skipped_rows > 0:
        log(f"  Skipped rows (bad data): {skipped_rows}")

    return records


def group_by_device(records):
    groups = {}

    for record in records:
        dev_id = record["device_id"]

        if dev_id not in groups:
            groups[dev_id] = {
                "temps": [],
                "statuses": [],
                "count": 0,
                "error_count": 0
            }

        groups[dev_id]["temps"].append(record["temperature"])
        groups[dev_id]["statuses"].append(record["status"])
        groups[dev_id]["count"] += 1

        if record["status"] == "ERROR":
            groups[dev_id]["error_count"] += 1

    return groups


def compute_statistics(groups):
    stats = {}

    for dev_id, data in groups.items():
        temps = data["temps"]
        count = data["count"]

        avg_temp = sum(temps) / len(temps)
        min_temp = min(temps)
        max_temp = max(temps)

        stats[dev_id] = {
            "total_records": count,
            "average_temperature": round(avg_temp, 2),
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "error_count": data["error_count"]
        }

    return stats


def filter_devices(stats, threshold=80.0):
    passed = {}
    filtered = {}

    for dev_id in sorted(stats.keys()):
        device_stats = stats[dev_id]

        if device_stats["average_temperature"] > threshold:
            filtered[dev_id] = device_stats
        else:
            passed[dev_id] = device_stats

    return passed, filtered


def build_summary_list(passed_devices):
    summary = []

    for dev_id in sorted(passed_devices.keys()):
        data = passed_devices[dev_id]
        summary.append({
            "device_id": dev_id,
            "total_records": data["total_records"],
            "average_temperature": data["average_temperature"],
            "error_count": data["error_count"]
        })

    return summary


def save_to_json(data, output_path):
    try:
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        log(f"\n  JSON output saved to '{output_path}'")
    except Exception as e:
        print(f"  Error: Could not write to '{output_path}': {e}")


def print_results(passed, filtered, threshold):
    print("\n")
    print("=" * 62)
    print("  DEVICE TELEMETRY SUMMARY REPORT")
    print(f"  Filter: Devices with avg temperature > {threshold}°C removed")
    print("=" * 62)

    if len(filtered) > 0:
        print(f"\n  Filtered out ({len(filtered)} device(s)):")
        for dev_id, data in filtered.items():
            avg = data["average_temperature"]
            print(f"    - {dev_id}: avg temp {avg}°C (exceeds {threshold}°C)")
    else:
        print("\n  No devices were filtered out.")

    print(f"\n  {'Device':<10} {'Records':<10} {'Avg Temp':<11} {'Min':<9} {'Max':<9} {'Errors':<8}")
    print("  " + "-" * 57)

    if len(passed) == 0:
        print("  No devices remaining after filter.")
    else:
        for dev_id in sorted(passed.keys()):
            d = passed[dev_id]
            print(f"  {dev_id:<10} {d['total_records']:<10} {d['average_temperature']:<11} {d['min_temperature']:<9} {d['max_temperature']:<9} {d['error_count']:<8}")

    total_records = sum(d["total_records"] for d in passed.values())
    total_errors = sum(d["error_count"] for d in passed.values())

    print("\n  " + "-" * 57)
    print(f"  Total: {len(passed)} device(s), {total_records} record(s), {total_errors} error(s)")

    if len(filtered) > 0:
        print(f"  Excluded: {len(filtered)} device(s) above {threshold}°C threshold")

    print("=" * 62)
    print()


def main():
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = "device_telemetry.csv"

    output_path = "summary_output.json"
    threshold = 80.0

    log(f"\n  Device Log Summarizer")
    log(f"  " + "-" * 30)
    log(f"  Input file:  {csv_path}")
    log(f"  Output file: {output_path}")
    log(f"  Threshold:   {threshold}°C")
    log()

    log("  [Step 1] Reading CSV file...")
    records = read_csv_file(csv_path)

    if len(records) == 0:
        print("\n  No valid records found. Nothing to process.")
        return

    log("\n  [Step 2] Grouping by device_id...")
    groups = group_by_device(records)
    log(f"  Found {len(groups)} unique device(s): {', '.join(sorted(groups.keys()))}")

    log("\n  [Step 3] Computing statistics...")
    stats = compute_statistics(groups)

    log(f"\n  [Step 4] Filtering devices (threshold: avg > {threshold}°C)...")
    passed, filtered = filter_devices(stats, threshold)

    log("\n  [Step 5] Exporting results...")
    summary_list = build_summary_list(passed)
    save_to_json(summary_list, output_path)

    print_results(passed, filtered, threshold)


if __name__ == "__main__":
    main()