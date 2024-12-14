import copy
import tqdm

# Read file.
with open('day6/aoc_day6.txt') as f:
	map = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Convert strings to list.
map = [list(r) for r in map]

# Find guard.
for r in range(len(map)):
	if '^' in map[r]:
		c = map[r].index('^')
		break

def rotate(dir):
	if dir == (-1, 0):
		return (0, 1)
	elif dir == (0, 1):
		return (1, 0)
	elif dir == (1, 0):
		return (0, -1)
	elif dir == (0, -1):
		return (-1, 0)

def print_map(the_map):
	for r in the_map:
		print(''.join(r))

def simulate_guard_path(map, start_pos):
	# Returns visited_map, positions_visited if there is not an infinite loop;
	# visited_map, None if there is.

	r, c = start_pos
	# Simulate guard path.
	positions_visited = 0
	visited_map = copy.deepcopy(map)
	done = False
	dir = (-1, 0)
	while not done:
		# Mark position on visted map.
		if visited_map[r][c] in ('^', '.', '#'):
			visited_map[r][c] = dir
			positions_visited += 1
		# Identify next position.
		next_pos = (r+dir[0], c+dir[1])
		# Did we leave the map?
		if 0 <= next_pos[0] < len(map) and 0 <= next_pos[1] < len(map[0]):
			if map[next_pos[0]][next_pos[1]] == '#':
				dir = rotate(dir)
			else:
				r, c = next_pos
				if visited_map[r][c] == dir:
					# Already visited this position, in the same direction ==> infinite loop.
					done = True
					inf_loop = True
		else:
			done = True
			inf_loop = False

	if inf_loop:
		return visited_map, None
	else:
		return visited_map, positions_visited

# PART 1

visted_map, positions_visited = simulate_guard_path(map, (r, c))

print(f'visted {positions_visited} positions')
# print()
# print_map(visited_map)

# PART 2

options = []
pbar = tqdm.tqdm(total=len(map) * len(map[0]))

start_pos = (r, c)

# Loop through positions.
for r in range(len(map)):
	for c in range(len(map[r])):
		pbar.update()
		if map[r][c] == '.':
			# Change to '#'.
			map[r][c] = '#'
			# Check for infinite loop.
			visted_map, positions_visited = simulate_guard_path(map, start_pos)
			if positions_visited is None:
				# Infinite loop -- add to options.
				options.append((r, c))
			# Change back to '.'.
			map[r][c] = '.'

print(f'{len(options)} options')