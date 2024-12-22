import functools

# Using the idea described here: https://www.reddit.com/r/adventofcode/comments/1hbnyx1/2024_day_11python_mega_tutorial/

# Read file.
with open('day11/aoc_day11.txt') as f:
	initial_stones = f.read().split()
# Convert strings to ints.
initial_stones = [int(s) for s in initial_stones]

NUM_BLINKS = 75

@functools.lru_cache(maxsize=None)
def single_blink_stone(value):
	"""Follows the stone rules and return the two resulting stone values
	(or the one, plus None)."""
	if value == 0:
		return 1, None
	elif len(str(value)) % 2 == 0:
		split_pt = int(len(str(value))/2)
		value1 = int(str(value)[:split_pt])
		value2 = int(str(value)[split_pt:])
		return value1, value2
	else:
		return value * 2024, None

@functools.lru_cache(maxsize=None)
def num_stones_after_blinks(value, num_blinks):
	"""Return the number of stones in the pile if we start with one stone engraved with
	`value` and do `num_blinks` blinks.
	Calls itself recursively, unless num_blinks == 0 (returns 1) or value is None (returns 0).
	"""

	if value is None:
		return 0
	elif num_blinks == 0:
		return 1
	else:
		# Do one blink.
		value1, value2 = single_blink_stone(value)
		# Call self on the resulting stones.
		return num_stones_after_blinks(value1, num_blinks - 1) + num_stones_after_blinks(value2, num_blinks - 1)
	

num_stones = 0
for s in initial_stones:
	num_stones += num_stones_after_blinks(s, NUM_BLINKS)

#print(f'after {NUM_BLINKS} blinks: {len(stones)} stones: {stones}')
print(f'after {NUM_BLINKS} blinks: {num_stones} stones')
