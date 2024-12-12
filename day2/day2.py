#import pandas as pd
import csv

# Read file.
with open('day2/aoc_day2_sample.csv') as f:
	reader = csv.reader(f, delimiter=' ')
	reports = [row for row in reader]

# Convert to numeric.
reports = [list(map(int, report)) for report in reports]

# PART 1

def is_safe(report):
	diffs = [report[n+1] - report[n] for n in range(len(report)-1)]
	if (all([diffs[n] < 0 for n in range(len(diffs))]) or all([diffs[n] > 0 for n in range(len(diffs))])) \
		and all([1 <= abs(diffs[n]) <= 3 for n in range(len(diffs))]):
		return True
	else:
		return False
	
# Count safe reports.
num_safe = 0
for report in reports:
	if is_safe(report):
		num_safe += 1

print(f'Number of safe reports = {num_safe}')

# PART 2

def is_safe_with_dampener(report):
	for m in range(len(report)):
		new_report = [report[n] for n in range(len(report)) if n != m]
		if is_safe(new_report):
			return True
	return False
	
# Count safe reports.
num_safe = 0
for report in reports:
	if is_safe_with_dampener(report):
		num_safe += 1

print(f'Number of safe reports with dampener = {num_safe}')


