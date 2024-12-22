import tqdm

DEBUG_MODE = True

# Read file.
with open('day11/aoc_day11.txt') as f:
	stones = f.read().split()
# Convert strings to ints.
stones = [int(s) for s in stones]
# Replace each stone with a list, which we'll add to to create the stone's descendants.
stones = [[s] for s in stones]

stones = [[0]]

if DEBUG_MODE:
	print(f'after 0 blinks ({sum([len(s_list) for s_list in stones])} stones): {stones}')
else:
	print(f'after 0 blinks: {sum([len(s_list) for s_list in stones])} stones')

num_blinks = 75

# VERSION 2:
# Handle one stone at a time, looping through blinks, then move on to the next one.

pbar = tqdm.tqdm(total=len(stones) * num_blinks)

for s, stone in enumerate(stones):

	for b in range(num_blinks):

		pbar.update()

		if DEBUG_MODE:
			print(f's = {s} b = {b}: {len(stones[s])}')

		# Loop through stones in this stone's list.
		t = 0
		while t < len(stones[s]):

			st = stones[s][t]

			# Apply rules.
			if st == 0:
				stones[s][t] = 1
			elif len(str(st)) % 2 == 0:
				split_pt = int(len(str(st))/2)
				stones[s][t] = int(str(st)[:split_pt])
				stones[s].insert(t+1, int(str(st)[split_pt:]))
				t += 1 # since we added a stone
			else:
				stones[s][t] = st * 2024

			t += 1

if DEBUG_MODE:
	print(f'after {b+1} blinks ({sum([len(s_list) for s_list in stones])} stones): {stones}')
else:
	print(f'after {b+1} blinks: {sum([len(s_list) for s_list in stones])} stones')



# VERSION 1:
# Handle one blink at a time, looping through stones.

def version_1(num_blinks, stones):
	# Loop through blinks.
	for b in range(num_blinks):

		# Make temp copy of stones.
		temp_stones = [s for s in stones]

		# Loop through stones. (Don't use for loop since current index changes during loop.)
		s = 0
		while s < len(temp_stones):

			stone = temp_stones[s]

			# Apply rules.
			if stone == 0:
				temp_stones[s] = 1
			elif len(str(stone)) % 2 == 0:
				split_pt = int(len(str(stone))/2)
				temp_stones[s] = int(str(stone)[:split_pt])
				temp_stones.insert(s+1, int(str(stone)[split_pt:]))
				s += 1 # since we added a stone
			else:
				temp_stones[s] = stone * 2024

			s += 1

		# Replace stones list.
		stones = temp_stones

		if DEBUG_MODE:
			print(f'after {b+1} blinks ({len(stones)} stones): {stones}')
		else:
			print(f'after {b+1} blinks: {len(stones)} stones')
