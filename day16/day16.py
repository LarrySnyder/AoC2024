# Use forward recursion, with help from https://github.com/fivard/AOC-2024/tree/master/day16.

import numpy as np
from collections import deque
import time
import tqdm

PART = 2
SAMPLE = False
if SAMPLE:
	FILENAME = 'day16/aoc_day16_sample.txt'
else:
	FILENAME = 'day16/aoc_day16.txt'

MOVE_COST = 1
TURN_COST = 1000
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# int literals for maze chars.
MAZE_WALL = -2
MAZE_PATH = -1
MAZE_START = -3
MAZE_END = -4
MAZE_OPT_TILE = -5

def read_data():
	with open(FILENAME) as f:
		maze = f.read().splitlines() # splitlines gets rid of \n at end of lines
	maze = [list(row) for row in maze]

	# Convert chars to ints.
	for r in range(len(maze)):
		for c in range(len(maze[r])):
			if maze[r][c] == '#':
				maze[r][c] = MAZE_WALL
			elif maze[r][c] == '.':
				maze[r][c] = MAZE_PATH
			elif maze[r][c] == 'S':
				maze[r][c] = MAZE_START
			elif maze[r][c] == 'E':
				maze[r][c] = MAZE_END

	# Convert to 2D np array.
	maze = np.vstack([np.array(list(row), dtype=int) for row in maze])

	return maze

def find_start_end(maze):
	start_pos = np.where(maze == MAZE_START)
	start_pos = (start_pos[0][0], start_pos[1][0])
	start_dir = (0, 1)
	end_pos = np.where(maze == MAZE_END)
	end_pos = (end_pos[0][0], end_pos[1][0])

	return start_pos, start_dir, end_pos

def turn(dir, turn_dir='L'):
	# Convert to polar.
	rho = 1
	phi = np.arctan2(dir[1], dir[0])
	# Rotate.
	if turn_dir == 'L':
		phi += np.pi / 2
	else:
		phi -= np.pi / 2
	# Convert back to rectangular.
	return (int(rho * np.cos(phi)), int(rho * np.sin(phi)))

def move(pos, dir):
	return tuple(np.array(pos) + np.array(dir))

def in_maze(maze, pos):
	return pos[0] >= 0 and pos[1] >= 0 and pos[0] < len(maze) and pos[1] < len(maze[0])

def pretty_print(maze):
	for r in range(len(maze)):
		for c in range(len(maze[0])):
			if maze[(r, c)] == MAZE_WALL:
				print('#', end='')
			elif maze[(r, c)] == MAZE_PATH:
				print('.', end='')
			elif maze[(r, c)] == MAZE_START:
				print('S', end='')
			elif maze[(r, c)] == MAZE_END:
				print('E', end='')
			elif maze[(r, c)] == MAZE_OPT_TILE:
				print('O', end='')
		print('')

def solve_maze(maze, force_start_dir=None, force_end_dir=None):
	# If force_start_dir is not None, path must leave start tile using that direction.
	# If force_end_dir is not None, path must enter end tile using that direction.
	# (Used for part 2.)

	# Find start and end.
	start_pos, start_dir, end_pos = find_start_end(maze)
	if force_start_dir:
		start_dir = force_start_dir

	# Initialize queue of pos/dir to check.
	queue = deque()
	start = (start_pos, start_dir, 0)
	queue.append(start)

	# Cost to reach starting position = 0.
	maze[start_pos] = 0

	while queue:

		# Get next item in queue.
		current = queue.popleft()
		curr_pos = current[0]
		curr_dir = current[1]
		curr_cost = current[2]

		# Directions we can go, and local cost of each.
		new_dirs_and_costs = (
			(curr_dir, curr_cost + MOVE_COST), 							# move straight
			(turn(curr_dir, 'L'), curr_cost + MOVE_COST + TURN_COST),	# turn left and move
			(turn(curr_dir, 'R'), curr_cost + MOVE_COST + TURN_COST)	# turn right and move
		)
		
		# Loop through directions.
		for new_dir, new_cost in new_dirs_and_costs:
			# Determine new position, and whether there's a wall there.
			new_pos = move(curr_pos, new_dir)
			if maze[new_pos] == MAZE_WALL:
				continue

			# Don't allow move if it goes into end tile from wrong direction.
			if new_pos == end_pos and force_end_dir and new_dir != force_end_dir:
				continue

			# If maze[new_pos] >= 0, we have already visited it and have a cost; compare to new cost.
			# If not, we haven't visited it yet; change its entry to the cost.
			# Either way, add new position and direction to queue.
			if (maze[new_pos] >= 0 and new_cost < maze[new_pos]) or maze[new_pos] in (MAZE_PATH, MAZE_END):
				maze[new_pos] = new_cost
				# Add new position to queue
				queue.append((new_pos, new_dir, new_cost))

	return maze[end_pos]

def num_tiles_on_optimal_path(maze):
	# Backtrack through optimal maze costs.

	# Find start and end.
	start_pos, start_dir, end_pos = find_start_end(maze)

	# Remember original maze.
	orig_maze = np.array(maze)

	# Solve maze.
	solve_maze(maze)

	# Initialize queue of pos/dir to check.
	queue = deque()
	# Find directions that lead into end.
	for dir in DIRECTIONS:
		if in_maze(maze, move(end_pos, dir)) and maze[move(end_pos, dir)] >= 0:
			# Cost to reach end position = maze[end_pos].
			queue.append((end_pos, dir, maze[end_pos]))

	# Initialize visited set.
	visited = set()
	opt_tiles = {end_pos}

	while queue:

		# Get next item in queue.
		current = queue.popleft()
		curr_pos = current[0]
		curr_dir = current[1]
		curr_cost = current[2]

		# Directions we can go, and (negative of) local cost of each.
		new_dirs_and_costs = (
			(curr_dir, curr_cost - MOVE_COST),
			(turn(curr_dir, 'L'), curr_cost - MOVE_COST - TURN_COST),
			(turn(curr_dir, 'R'), curr_cost - MOVE_COST - TURN_COST)
		)

		# Loop through directions.
		for new_dir, new_cost in new_dirs_and_costs:
			# Determine new position, and whether there's a wall there.
			new_pos = move(curr_pos, new_dir)
			if maze[new_pos] == MAZE_WALL:
				continue

			# If maze[new_pos] == new_cost, this is an optimal tile; 
			# if new_pos is not visited, add it.
			if (new_pos not in visited) and (maze[new_pos] in (new_cost, new_cost - TURN_COST)):
				opt_tiles.add(new_pos)
				queue.append((new_pos, new_dir, new_cost))
				visited.add(new_pos)

	# Print map of opitmal tiles.
	final_maze = np.array(orig_maze)
	for r in range(len(maze)):
		for c in range(len(maze[0])):
			if (r, c) in opt_tiles:
				final_maze[(r, c)] = MAZE_OPT_TILE
	pretty_print(final_maze)

	return len(opt_tiles)


	

def num_tiles_on_optimal_path_old(maze):
	# Strategy: for each non-wall tile in maze, if the optimal cost from start to tile 
	# plus optimal cost from tile to end equals overall optimal cost, the tile is on an
	# optimal path. Need to check all possible in- and out-directions to tile.

	# Solve overall problem to get overall optimal. (Use local copy to avoid overwriting tile values.)
	temp_maze = np.array(maze)
	opt_cost = solve_maze(temp_maze)

	# Find start and end.
	start_pos, _, end_pos = find_start_end(maze)

	pbar = tqdm.tqdm(total=len(maze) * len(maze[0]))

	# Loop through tiles.
	opt_tiles = []
	for r in range(len(maze)):
		for c in range(len(maze[0])):
			pbar.update()
			if maze[(r, c)] in (MAZE_START, MAZE_END):
				# Start and end tiles are always optimal (and logic below might fail on them).
				opt_tiles.append((r, c))
			elif maze[(r, c)] == MAZE_PATH:
				for dir in DIRECTIONS:
					# Can we even enter from this direction?
					back_one = tuple(np.array((r, c)) + np.array(dir))
					if maze[back_one] == MAZE_WALL:
						continue
					# Make copy of maze where end = tile.
					temp_maze = np.array(maze)
					temp_maze[end_pos] = MAZE_PATH
					temp_maze[(r, c)] = MAZE_END
					# Solve, forcing end direction to equal dir.
					cost_in = solve_maze(temp_maze, force_end_dir=dir)

					# Make copy of maze where start = tile.
					temp_maze = np.array(maze)
					temp_maze[start_pos] = MAZE_PATH
					temp_maze[(r, c)] = MAZE_START
					# Solve, forcing start direction to equal dir.
					cost_out = solve_maze(temp_maze, force_start_dir=dir)

					# Is total cost the same?
					if cost_in + cost_out == opt_cost:
						opt_tiles.append((r, c))
						break # don't try other directions

	# Print map of optimal tiles.
	final_maze = np.array(maze)
	ttmep = 0
	for r in range(len(maze)):
		for c in range(len(maze[0])):
			if (r, c) in opt_tiles:
				final_maze[(r, c)] = MAZE_OPT_TILE
				ttmep += 1
	pretty_print(final_maze)

	return len(opt_tiles)

		
def solve_aoc():
	maze = read_data()
	if PART == 1:
		result = solve_maze(maze)
	else:
		result = num_tiles_on_optimal_path(maze)
	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")