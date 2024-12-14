# Read file.
with open('day4/aoc_day4.txt') as f:
	puz = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Directions to search.
DIRS = ((-1, -1), (-1, 0), (-1, 1), 
		(0, -1), (0, 1),
		(1, -1), (1, 0), (1, 1))

# PART 1

# Go row-by-row, column-by-column, and stop at each 'X'.
row = 0
col = 0
num_finds = 0
while row < len(puz):
	while col < len(puz[row]):
		if puz[row][col] == 'X':
			# Found an 'X'. Look in each direction.
			for dir in DIRS:
				delta_r, delta_c = dir
				if 0 <= row+3*delta_r < len(puz) and 0 <= col+3*delta_c < len(puz[row]):
#				try: # skip errors due to going out of puzzle bounds
					if puz[row+delta_r][col+delta_c] == 'M' and \
						puz[row+2*delta_r][col+2*delta_c] == 'A' and \
						puz[row+3*delta_r][col+3*delta_c] == 'S':
						num_finds += 1
				# except:
				# 	pass
		# Move to next col.
		col += 1
	# Move to next row.
	row += 1
	col = 0

print(f'num XMASes = {num_finds}')

# PART 2

num_finds = 0
for row in range(1, len(puz)-1):
	for col in range(1, len(puz[row])-1):
		if puz[row][col] == 'A':
			if {puz[row-1][col-1], puz[row+1][col+1]} == {'M', 'S'} and \
				{puz[row-1][col+1], puz[row+1][col-1]} == {'M', 'S'}:
				num_finds += 1

print(f'num X-MASes = {num_finds}')
