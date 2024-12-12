import pandas as pd
from collections import Counter

# Read file.
df = pd.read_csv('day1/aoc_day1.csv', delim_whitespace=True, header=None)

list1 = df[0].to_list()
list2 = df[1].to_list()

# Sort lists.
list1.sort()
list2.sort()

# PART 1

# Calculate sum of differences.
sum_of_diffs = sum([abs(list1[n] - list2[n]) for n in range(len(list1))])

print(f'sum of differences = {sum_of_diffs}')

# PART 2

# Build counter.
ctr = Counter(list2)

# Calculate similarity score.
sim_score = 0
for item in list1:
	sim_score += item * ctr[item]

print(f'similarity score = {sim_score}')