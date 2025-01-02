import numpy as np
import time
import tqdm
import functools


PART = 2
SAMPLE = False
if SAMPLE:
	FILENAME = 'day19/aoc_day19_sample.txt'
else:
	FILENAME = 'day19/aoc_day19.txt'

def read_data():
	with open(FILENAME) as f:
		info = f.read().splitlines() # splitlines gets rid of \n at end of lines
	
	towel_patterns = info[0].split(', ')
	desired_designs = info[2:]

	return towel_patterns, desired_designs

@functools.lru_cache(maxsize=None)
def build_design(design):
	if design == '':
		return []
	
	# Determine all towels that fit the next sequence.
	for t in towel_patterns:
		if design[:len(t)] == t:
			next_towels = build_design(design[len(t):])
			if next_towels is not None:
				return [t] + next_towels
			
	return None

@functools.lru_cache(maxsize=None)
def build_design_all(design):
	# Determine all towels that fit the next sequence.
	num_sequences = 0
	for t in towel_patterns:
		if design == t:
			num_sequences += 1
		elif design[:len(t)] == t:
			num_sequences += build_design_all(design[len(t):])

	return num_sequences

def solve_puzzle(desired_designs):
	pbar = tqdm.tqdm(total=len(desired_designs))

	# Try each desired design.
	num_possible_designs = 0
	for design in desired_designs:
		pbar.update()
		if PART == 1:
			if build_design(design) is not None:
				num_possible_designs += 1
				print(f'design: {design:60} YES')
			else:
				print(f'design: {design:60} NO')
		else:
			num_designs = build_design_all(design)
			num_possible_designs += num_designs
			print(f'design: {design:60} {num_designs}')

	return num_possible_designs



def solve_aoc():
	global towel_patterns
	towel_patterns, desired_designed = read_data()
	result = solve_puzzle(desired_designed)
	# else:
	# 	result = find_cut_byte(byte_positions)
	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
