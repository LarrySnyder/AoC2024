# Read file.
with open('day10/aoc_day10.txt') as f:
	map = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Convert strings to list.
map = [[-1 if val == '.' else int(val) for val in r] for r in map]

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def reachable_9s(map, loc, part):
	"""Determine set of reachable 9s from 'loc'. Calls itself recursively.
	If part = 1, returns set of reachable 9s; if part = 2, returns number
	of reachable 9s (which means it will count distinct paths to each 9).
	"""

	# Determine value at loc.
	val = map[loc[0]][loc[1]]

	if val == 9:
		# We're done. 
		if part == 1:
			return {loc}
		else:
			return 1

	# Find all neighboring locations with val+1.
	if part == 1:
		set_of_9s = set()
	else:
		set_of_9s = 0
	for dir in DIRECTIONS:
		new_loc = (loc[0] + dir[0], loc[1] + dir[1])
		if 0 <= new_loc[0] < len(map) and 0 <= new_loc[1] < len(map[0]):
			if map[new_loc[0]][new_loc[1]] == val + 1:
				new_9s = reachable_9s(map, new_loc, part)
				if part == 1:
					set_of_9s = set_of_9s.union(new_9s)
				else:
					set_of_9s += new_9s

	return set_of_9s

# PART 1

trailheads = []
for r in range(len(map)):
	for c in range(len(map[r])):
		if map[r][c] == 0:
			set_of_9s = reachable_9s(map, (r, c), 1)
			trailheads.append(((r, c), len(set_of_9s), set_of_9s))

print('PART 1 TRAILHEADS:')
for tr in trailheads:
	print(f'{tr[0]}: score = {tr[1]}')
print(f'sum of scores = {sum([tr[1] for tr in trailheads])}')

# PART 2

trailheads = []
for r in range(len(map)):
	for c in range(len(map[r])):
		if map[r][c] == 0:
			set_of_9s = reachable_9s(map, (r, c), 2)
			trailheads.append(((r, c), set_of_9s))

print('PART 2 TRAILHEADS:')
for tr in trailheads:
	print(f'{tr[0]}: rating = {tr[1]}')
print(f'sum of ratings = {sum([tr[1] for tr in trailheads])}')