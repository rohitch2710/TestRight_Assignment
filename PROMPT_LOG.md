# PROMPT_LOG

## My Initial Prompt to the AI

I used ChatGPT and gave it this prompt:

> Write a Python script using matplotlib that reads a JSON file called summary_output.json containing device data with fields device_id, total_records, average_temperature, and error_count. Generate a bar chart comparing the average temperature for each device and save it as a PNG image.

## What Was Wrong With the First Output

The AI gave me a basic working script but it had a few problems when I actually ran it:

1. Labels getting cut off - The temperature labels that it put on top of each bar were getting clipped because the y-axis range was automatically set to just the max value. So the tallest bar's label was literally outside the visible area of the chart.

2. No visual distinction between devices - All the bars were the same default blue color. Looking at the chart you couldn't quickly tell which devices were running hot vs cool without reading every single number.

3. No context about the 80 degree filter - Since our summarizer filters out devices above 80°C, it would be useful to show that threshold on the chart. But the AI didn't include any reference line.

4. Missing information - It only showed the temperature on each bar. I also wanted to see the error count and record count since thats useful context from the data.

## My Follow-Up Prompt to Fix These Issues

> The chart has some issues. Fix these:
> 1. The y-axis is too tight and the labels on top of bars get cut off. Set ylim to about 35% above the max temperature value.
> 2. Color code the bars by temperature range - green for under 30, blue for 30-50, orange for 50-70, red for 70-80.
> 3. Add a red dashed horizontal line at 80 degrees with a label saying "80°C threshold".
> 4. Show the error count and record count as additional lines in the bar label, not just the temperature.
> 5. Add a legend explaining what each color means.

After applying these fixes the chart was much more informative and all the labels were properly visible.
