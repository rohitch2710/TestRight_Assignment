import json
import os
import matplotlib.pyplot as plt

input_file = "summary_output.json"

if not os.path.exists(input_file):
    print(f"Error: '{input_file}' not found.")
    print("Run summarizer.py first to generate the JSON file.")
    exit(1)

with open(input_file, "r") as f:
    data = json.load(f)

if len(data) == 0:
    print("No data to plot - the JSON file is empty.")
    exit(0)

devices = [item["device_id"] for item in data]
avg_temps = [item["average_temperature"] for item in data]
error_counts = [item["error_count"] for item in data]
record_counts = [item["total_records"] for item in data]

colors = []
for temp in avg_temps:
    if temp < 30:
        colors.append("#27ae60")   
    elif temp < 50:
        colors.append("#2980b9")   
    elif temp < 70:
        colors.append("#f39c12")   
    else:
        colors.append("#e74c3c")   

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(devices, avg_temps, color=colors, edgecolor="black",
              linewidth=0.8, width=0.5)

for i, bar in enumerate(bars):
    height = bar.get_height()

    label_parts = [f"{height}°C"]
    if error_counts[i] > 0:
        label_parts.append(f"{error_counts[i]} error(s)")
    label_parts.append(f"{record_counts[i]} records")
    label_text = "\n".join(label_parts)

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1.5,
        label_text,
        ha="center",
        va="bottom",
        fontsize=8.5,
        fontweight="bold",
        color="#333333"
    )

ax.set_title("Average Temperature per Device\n(Devices exceeding 80°C have been filtered out)",
             fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Device ID", fontsize=11, labelpad=8)
ax.set_ylabel("Average Temperature (°C)", fontsize=11, labelpad=8)

max_temp = max(avg_temps)
ax.set_ylim(0, max_temp * 1.35)

ax.grid(axis="y", linestyle="--", alpha=0.4, color="gray")
ax.set_axisbelow(True)  

ax.axhline(y=80.0, color="#c0392b", linestyle=":", linewidth=1.5, alpha=0.8)
ax.text(len(devices) - 0.3, 81.5, "80°C threshold", color="#c0392b",
        fontsize=8, ha="right", fontstyle="italic")

from matplotlib.patches import Patch
legend_items = [
    Patch(facecolor="#27ae60", edgecolor="black", label="< 30°C (Cool)"),
    Patch(facecolor="#2980b9", edgecolor="black", label="30-50°C (Normal)"),
    Patch(facecolor="#f39c12", edgecolor="black", label="50-70°C (Warm)"),
    Patch(facecolor="#e74c3c", edgecolor="black", label="70-80°C (Hot)")
]
ax.legend(handles=legend_items, loc="upper left", fontsize=8,
          framealpha=0.9, edgecolor="gray")

plt.tight_layout()

output_file = "device_temperatures.png"
plt.savefig(output_file, dpi=200, bbox_inches="tight")
plt.close()

print(f"Chart saved as '{output_file}'")
print(f"Plotted {len(devices)} device(s)")
