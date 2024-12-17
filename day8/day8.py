import itertools


def find_antennas(map):
	antennas = {}
	for r in range(len(map)):
		for c in range(len(map[r])):
			cell = map[r][c]
			if cell != '.':
				if cell in antennas:
					antennas[cell].append((r, c))
				else:
					antennas[cell] = [(r, c)]

	return antennas

def is_in_map(point, map):
	if 0 <= point[0] < len(map) and 0 <= point[1] < len(map[0]):
		return True
	else:
		return False

# Read file.
with open('day8/aoc_day8.txt') as f:
	map = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Convert strings to list.
map = [list(r) for r in map]

# PART 1

def find_antinodes_part1(map, antennas):
	antinodes = set()
	for freq in antennas:
		for (antenna1, antenna2) in itertools.combinations(antennas[freq], 2):
			# Determine distance vector between antennas.
			dist = (antenna1[0] - antenna2[0], antenna1[1] - antenna2[1])
			# Find antinodes.
			antinode1 = (antenna1[0] + dist[0], antenna1[1] + dist[1])
			antinode2 = (antenna2[0] - dist[0], antenna2[1] - dist[1])
			# Add to dict.
			if is_in_map(antinode1, map):
				antinodes.add(antinode1)
			if is_in_map(antinode2, map):
				antinodes.add(antinode2)

	return antinodes

# Find antinodes.
antennas = find_antennas(map)
antinodes = find_antinodes_part1(map, antennas)

print(f'Part 1: there are {len(antinodes)} unique antinodes')


# PART 2

def find_antinodes_part2(map, antennas):
	antinodes = set()
	for freq in antennas:
		for (antenna1, antenna2) in itertools.combinations(antennas[freq], 2):
			# Determine distance vector between antennas.
			dist = (antenna1[0] - antenna2[0], antenna1[1] - antenna2[1])
			# Find antinodes.
			antinode1 = antenna1
			while is_in_map(antinode1, map):
				antinodes.add(antinode1)
				antinode1 = (antinode1[0] + dist[0], antinode1[1] + dist[1])
			antinode2 = antenna2
			while is_in_map(antinode2, map):
				antinodes.add(antinode2)
				antinode2 = (antinode2[0] - dist[0], antinode2[1] - dist[1])

	return antinodes

# Find antinodes.
antennas = find_antennas(map)
antinodes = find_antinodes_part2(map, antennas)

print(f'Part 2: there are {len(antinodes)} unique antinodes')

