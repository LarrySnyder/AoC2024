import numpy as np
import time
import networkx as nx


PART = 1
SAMPLE = False
NUM_BYTES = 2936
if SAMPLE:
	FILENAME = 'day18/aoc_day18_sample.txt'
	SIZE = 7
else:
	FILENAME = 'day18/aoc_day18.txt'
	SIZE = 71

def read_data():
	with open(FILENAME) as f:
		info = f.read().splitlines() # splitlines gets rid of \n at end of lines
	
	byte_positions = [row.split(',') for row in info]
	byte_positions = [(int(row[0]), int(row[1])) for row in byte_positions]

	return byte_positions

def solve_puzzle(byte_positions):
	# Create memory space.
	G = nx.DiGraph()
	G.add_nodes_from([(x, y) for x in range(SIZE) for y in range(SIZE)])

	# Add edges.
	for x in range(SIZE):
		for y in range(SIZE):
			if x > 0:
				if (x - 1, y) not in byte_positions:
					G.add_edge((x, y), (x - 1, y), weight=1)
			if x < SIZE - 1:
				if (x + 1, y) not in byte_positions:
					G.add_edge((x, y), (x + 1, y), weight=1)
			if y > 0:
				if (x, y - 1) not in byte_positions:
					G.add_edge((x, y), (x, y - 1), weight=1)
			if y < SIZE - 1:
				if (x, y + 1) not in byte_positions:
					G.add_edge((x, y), (x, y + 1), weight=1)

	# Find shortest path.
	sp = nx.shortest_path(G, source=(0, 0), target=(SIZE - 1, SIZE - 1), weight='weight')

#	print_map(byte_positions, sp)

	if sp is None:
		return None
	else:
		return len(sp) - 1

def find_cut_byte(byte_positions):
	lo = 0
	hi = len(byte_positions)
	mid = (lo + hi) // 2
	while True:
		print(f'lo = {lo:4} hi = {hi:4} mid = {mid:4}')
		try:
			solve_puzzle(byte_positions[:mid])
			lo = mid
		except nx.exception.NetworkXNoPath:
			hi = mid
		mid = (lo + hi) // 2
		if lo == mid or hi == mid:
			break

	return byte_positions[mid]



def print_map(byte_positions, sp=None):
	for y in range(SIZE):
		for x in range(SIZE):
			if sp is not None and (x, y) in sp:
				print('O', end='')
			elif (x, y) in byte_positions:
				print('#', end='')
			else:
				print('.', end='')
		print('')

def solve_aoc():
	byte_positions = read_data()
	if PART == 1:
		result = solve_puzzle(byte_positions[0:NUM_BYTES])
	else:
		result = find_cut_byte(byte_positions)
	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
