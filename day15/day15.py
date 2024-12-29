import numpy as np

PART = 2
DIRECTIONS = {'^': np.array((-1, 0)), '>': np.array((0, 1)), '<': np.array((0, -1)), 'v': np.array((1, 0))}

# Read map file.
with open('day15/aoc_day15_map.txt') as f:
	map = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Convert to 2D np array.
map = np.vstack([np.array(list(row)) for row in map])

# Build part-2 map, if part 2.
if PART == 2:
	map2 = []
	for row in map:
		row2 = ''
		for tile in row:
			if tile == '#':
				row2 += '##'
			elif tile == 'O':
				row2 += '[]'
			elif tile == '.':
				row2 += '..'
			elif tile == '@':
				row2 += '@.'
		map2.append(row2)
	map = np.vstack([np.array(list(row2)) for row2 in map2])

# Read directions file.
with open('day15/aoc_day15_directions.txt') as f:
	dir_file = f.read().splitlines()

# Combine into one string.
directions = ''
for row in dir_file:
	directions += row

# Find robot.
init_pos = np.where(map == '@')
init_pos = np.array([init_pos[0][0], init_pos[1][0]])

N_ROWS = len(map)
N_COLS = len(map[0])

def move_part_1(map, pos, dir):
	# Count boxes between pos and next . or #.
	non_box = 1
	while map[tuple(pos + non_box * DIRECTIONS[dir])] == 'O':
		non_box += 1

	# What is first non-box space?
	if map[tuple(pos + non_box * DIRECTIONS[dir])] == '#':
		# We can't move; do nothing.
		new_pos = pos
	else:
		# First non-box space is '.'
		for n in range(1, non_box):
			map[tuple(pos + (n + 1) * DIRECTIONS[dir])] = 'O'
		new_pos = tuple(pos + DIRECTIONS[dir])
		map[new_pos] = '@'
		map[tuple(pos)] = '.'
	 
	return map, new_pos

def move_part_2(map, pos, dir):
	# First non-box space is '.'
	if dir in ('<', '>'):
		# Count boxes between pos and next . or #.
		non_box = 1
		while map[tuple(pos + non_box * DIRECTIONS[dir])] in ('[', ']'):
			non_box += 1

		# What is first non-box space?
		if map[tuple(pos + non_box * DIRECTIONS[dir])] == '#':
			# We can't move; do nothing.
			new_pos = pos
		else:
			for n in range(non_box, 0, -1):
				map[(tuple(pos + n * DIRECTIONS[dir]))] = map[(tuple(pos + (n - 1) * DIRECTIONS[dir]))]
			new_pos = tuple(pos + DIRECTIONS[dir])
			map[new_pos] = '@'
			map[tuple(pos)] = '.'
	else:
		# Identify left-hand coordinate of boxes that would be pushed. 
		done2 = False
		can_push = True
		pushed_tiles = set()
		pushing_tiles = {tuple(pos)}
		while not done2:
			new_pushing_tiles = set()
			new_pushed_tiles = set()
			# Are there any boxes that would be pushed by any tiles in pushing_tiles?
			for t in pushing_tiles:
				next_tile = map[(tuple(t + DIRECTIONS[dir]))]
				if next_tile in ('[', ']'):
					if next_tile == '[':
						new_tiles_pushed = {tuple(t + DIRECTIONS[dir]), tuple(t + DIRECTIONS[dir] + DIRECTIONS['>'])}
					elif next_tile == ']':
						new_tiles_pushed = {tuple(t + DIRECTIONS[dir]), tuple(t + DIRECTIONS[dir] + DIRECTIONS['<'])}
					new_pushed_tiles.update(new_tiles_pushed)
					new_pushing_tiles.update(new_tiles_pushed)
				elif next_tile == '#':
					done2 = True
					can_push = False
					break
			# Update arrays.
			pushing_tiles = new_pushing_tiles
			pushed_tiles.update(new_pushed_tiles)
			if len(new_pushed_tiles) == 0:
				done2 = True
		
		# Can we push?
		if can_push:
			rows_pushed = {t[0] for t in pushed_tiles}
			if rows_pushed:
				row_range = range(min(rows_pushed), max(rows_pushed) + 1) if dir == '^' else range(max(rows_pushed), min(rows_pushed) - 1, -1)
				for r in row_range:
					for t in pushed_tiles:
						if t[0] == r:
							map[tuple(t + DIRECTIONS[dir])] = map[tuple(t)]
							map[tuple(t)] = '.'
			new_pos = tuple(pos + DIRECTIONS[dir])
			map[new_pos] = '@'
			map[tuple(pos)] = '.'
		else:
			new_pos = pos

	return map, new_pos

def count_boxes(map):
	num_boxes = 0
	for row in map:
		for tile in row:
			if tile in ('O', '['):
				num_boxes += 1
	return num_boxes

def print_map(map, dir=None):
	if dir:
		print(f'Move {dir}:')
	for row in map:
		print(''.join(row))
	print('')

def gps_sum(map):
	sum_of_coords = 0
	for r in range(len(map)):
		for c in range(len(map[0])):
			if map[(r, c)] in ('O', '['):
				sum_of_coords += 100 * r + c
	
	return sum_of_coords

def simulate(map, init_pos):
	pos = init_pos
	
	for d, dir in enumerate(directions):

		if PART == 1:
			map, pos = move_part_1(map, pos, dir)
		else:
			map, pos = move_part_2(map, pos, dir)

#		print(f"{d:5} dir = {dir} num boxes = {count_boxes(map)}")

#		print_map(map, dir)

	return map

map = simulate(map, init_pos)

print_map(map)
print(f'Sum of GPS coordinates = {gps_sum(map)}')
