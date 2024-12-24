import networkx as nx

# Read file.
with open('day12/aoc_day12.txt') as f:
	map = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Convert strings to list.
map = [list(r) for r in map]

map_size = len(map)

# Build networkx representation of map.
G = nx.Graph()
# Add nodes.
for r, row in enumerate(map):
	for c, plant_type in enumerate(row):
		G.add_node((r, c), plant_type=plant_type)
# Add edges.
for r, row in enumerate(map):
	for c, plant_type in enumerate(row):
		# Add edges to nodes that are below or to the right.
		if c < len(row) - 1 and map[r][c + 1] == plant_type:
			G.add_edge((r, c), (r, c + 1))
		if r < len(map) - 1 and map[r + 1][c] == plant_type:
			G.add_edge((r, c), (r + 1, c))

# Initialize list of regions. Each element in list will contain tuple (plant_type, area, perimeter).
regions = []
total_price = 0

# Get all connected components.
components =  list(nx.connected_components(G))

# PART 1

print('------- PART 1 -------\n')

# Loop through components and analyze each.
for comp in components:

	area = len(comp)
	perim = 0

	# Loop through nodes in component.
	for node in comp:

		r, c = node

		# Count perimeter units.
		if r == 0 or (r-1, c) not in comp:
			perim += 1
		if c == 0 or (r, c-1) not in comp:
			perim += 1
		if c == map_size - 1 or (r, c+1) not in comp:
			perim += 1
		if r == map_size - 1 or (r+1, c) not in comp:
			perim += 1

	plant_type = map[node[0]][node[1]]


	regions.append((plant_type, area, perim))

	total_price += area * perim

	print(f'A region of {plant_type} plants with price {area} * {perim} = {area * perim}')

print(f'Total price = {total_price}')


# PART 2

print('\n------- PART 2 -------\n')

def has_border(component, map_size, r, c, direction):
	if r < 0 or c < 0 or r >= map_size or c >= map_size:
		return False
	
	if direction == 'N':
		return (r == 0 or (r-1, c) not in component)
	if direction == 'W':
		return (c == 0 or (r, c-1) not in component)
	if direction == 'E':
		return (c == map_size - 1 or (r, c+1) not in component)
	if direction == 'S':
		return (r == map_size - 1 or (r+1, c) not in component)
	
def is_type(map, r, c, plant_type):
	if r < 0 or c < 0 or r >= len(map) or c >= len(map):
		return False
	else:
		return map[r][c] == plant_type
	
def count_start_of_sides(component, map, r, c):
	"""Counts how many sides start at this node; side starts are always at the north or west of a side."""
	num_starts = 0
	map_size = len(map)
	plant_type = map[r][c]
	
	if has_border(component, map_size, r, c, 'N') and \
		(not is_type(map, r, c-1, plant_type) or is_type(map, r-1, c-1, plant_type)):
		num_starts += 1
	if has_border(component, map_size, r, c, 'W') and \
		(not is_type(map, r-1, c, plant_type) or is_type(map, r-1, c-1, plant_type)):
		num_starts += 1
	if has_border(component, map_size, r, c, 'E') and \
		(not is_type(map, r-1, c, plant_type) or is_type(map, r-1, c+1, plant_type)):
		num_starts += 1
	if has_border(component, map_size, r, c, 'S') and \
		(not is_type(map, r, c-1, plant_type) or is_type(map, r+1, c-1, plant_type)):
		num_starts += 1

	return num_starts
	

total_price = 0

# Loop through components and analyze each.
for comp in components:

	area = len(comp)
	sides = 0

	# Loop through nodes in component.
	for node in comp:

		r, c = node

		sides += count_start_of_sides(comp, map, r, c)

		plant_type = map[node[0]][node[1]]

	regions.append((plant_type, area, perim))

	total_price += area * sides

	print(f'A region of {plant_type} plants with price {area} * {sides} = {area * sides}')

print(f'Total price = {total_price}')