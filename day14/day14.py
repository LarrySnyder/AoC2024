import numpy as np

# Read file.
with open('day14/aoc_day14.txt') as f:
	input = f.read().splitlines() # splitlines gets rid of \n at end of lines

PART = 2
NUM_SECONDS = 100
WIDTH = 101
HEIGHT = 103

class Robot:
	def __init__(self, pos, vel):
		self.pos = pos
		self.vel = vel

def robot_count(robots):
	num_robots = {(x, y): 0 for x in range(WIDTH) for y in range(HEIGHT)}
	for r in robots:
		num_robots[(r.pos[0], r.pos[1])] += 1	
	return num_robots
	
def print_map(num_robots):
	for y in range(HEIGHT):
		for x in range(WIDTH):
			if num_robots[(x, y)] == 0:
				print('.', end='')
			else:
				print(f'{num_robots[(x, y)]}', end='')
		print('')

def calc_safety_factor(num_robots):
	quadrant_count = [0] * 4
	for x in range(WIDTH):
		for y in range(HEIGHT):
			if x < (WIDTH - 1) // 2:
				if y < (HEIGHT - 1) // 2:
					quadrant_count[0] += num_robots[(x, y)]
				elif y > (HEIGHT - 1) // 2:
					quadrant_count[1] += num_robots[(x, y)]
			elif x > (WIDTH - 1) // 2:
				if y < (HEIGHT - 1) // 2:
					quadrant_count[2] += num_robots[(x, y)]
				elif y > (HEIGHT - 1) // 2:
					quadrant_count[3] += num_robots[(x, y)]
	return np.product(quadrant_count)

# Parse input.
robots = []
for row in input:
	posx_start = int(row.find('p=')) + 2
	posy_start = int(row.find(',')) + 1
	space = int(row.find(' '))
	velx_start = int(row.find('v=')) + 2
	vely_start = int(row.find(',', velx_start)) + 1
	pos = np.array([int(row[posx_start:posy_start-1]), int(row[posy_start:space])])
	vel = np.array([int(row[velx_start:vely_start-1]), int(row[vely_start:])])

	robots.append(Robot(pos, vel))

def is_tree(num_robots):
	# Look for a row with >=10 (?) robots in a row, and 9 above it.
	found = False
	for y in range(4, HEIGHT):
		for x in range(WIDTH - 10):
			if all([num_robots[(m, y)] > 0 for m in range(x, x+10)]):
				found = True
				break
		if found:
			found = False
			for x in range(WIDTH - 9):
				if all([num_robots[(m, y-1)] > 0 for m in range(x, x+9)]):
					found = True
					break
		if found:
			break

	return found

def next_iter(robots):
	for r in robots:
		new_pos = r.pos + r.vel
		if new_pos[0] < 0:
			new_pos[0] = WIDTH + new_pos[0]
		if new_pos[0] >= WIDTH:
			new_pos[0] = new_pos[0] - WIDTH
		if new_pos[1] < 0:
			new_pos[1] = HEIGHT + new_pos[1]
		if new_pos[1] >= HEIGHT:
			new_pos[1] = new_pos[1] - HEIGHT
		r.pos = new_pos


if PART == 1:
	for t in range(NUM_SECONDS):
		next_iter(robots)

	num_robots = robot_count(robots)
	print_map(num_robots)
	sf = calc_safety_factor(num_robots)
	print(f'Safety factor = {sf}')

else:
	found = False
	for t in range(10000000):
		if t % 100 == 0:
			print(f't = {t}')
			
		num_robots = robot_count(robots)
		if is_tree(num_robots):
			found = True
			break
		else:
			next_iter(robots)
	
	if found:
		print(f'FOUND at second {t}')
	else:
		print(f'NOT FOUND')

	
