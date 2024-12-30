# Tried using backward recursion; not sure why it didn't work...

import numpy as np
import functools
import sys

# Change max recursion depth.
sys.setrecursionlimit(20000)

MOVE_COST = 1
TURN_COST = 1000
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

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

# DP, with memoization.
@functools.lru_cache(maxsize=None)
def maze_DP(pos, dir):
#	print(f'{pos} {dir}')

	if pos == end_pos:
		return 0
	elif visited[pos, dir]:
		# Already visited this node/direction -- don't keep looping.
		return np.inf
	
	visited[pos, dir] = True
	best_cost = np.inf

	# Test 3 options: move in the current direction, turn left and move, or turn right and move.
	new_pos_dir = (
		(tuple(np.array(pos) + np.array(dir)), dir),						# move
		(tuple(np.array(pos) + np.array(turn(dir, 'L'))), turn(dir, 'L')),	# left
		(tuple(np.array(pos) + np.array(turn(dir, 'R'))), turn(dir, 'R'))	# right
	)
	best_cost = np.inf
	for new_pos, new_dir in new_pos_dir:
		if maze[new_pos] == '#':
			continue
		cost = maze_DP(new_pos, new_dir) + MOVE_COST
		if new_dir != dir:
			cost += TURN_COST
		best_cost = min(cost, best_cost)

	# # Move.
	# new_pos = tuple(np.array(pos) + np.array(dir))
	# if maze[new_pos] == '#':
	# 	cost_move = np.inf
	# else:
	# 	cost_move = MOVE_COST + maze_DP(new_pos, dir)
	# # Turn left.
	# cost_left = TURN_COST + maze_DP(pos, turn(dir, 'L'))
	# # Turn right.
	# cost_right = TURN_COST + maze_DP(pos, turn(dir, 'R'))
		
	# best_cost = min(cost_move, cost_left, cost_right)
		
	visited[pos, dir] = False

	return best_cost

# ---------------

# Read map file.
with open('day16/aoc_day16.txt') as f:
	maze = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Convert to 2D np array.
maze = np.vstack([np.array(list(row)) for row in maze])

# Find start and end.
start_pos = np.where(maze == 'S')
start_pos = (start_pos[0][0], start_pos[1][0])
start_dir = (0, 1)
end_pos = np.where(maze == 'E')
end_pos = (end_pos[0][0], end_pos[1][0])

# Initialize visited array.
visited = {((r, c), d): False for r in range(len(maze)) for c in range(len(maze[0])) for d in DIRECTIONS}

# Solve maze.
best_cost = maze_DP(start_pos, start_dir)

print(f'best cost = {best_cost}')