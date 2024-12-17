# Read file.
with open('day9/aoc_day9.txt') as f:
	disk_map = f.read()
# Convert string to list.
disk_map = [int(r) for r in disk_map]

# PART 1

def expand_disk_map1(disk_map):
	# Expand disk_map into block representation.
	id = 0
	block_list = []
	for pos, digit in enumerate(disk_map):
		# Even => file, odd => free space.
		if pos % 2 == 0:
			block_list += [id] * digit
			id += 1
		else:
			block_list += ['.'] * digit

	return block_list

def compress_disk_map1(block_list):
	last_digit_pos = len(block_list) - 1

	# Loop through string, find '.'.
	for pos, digit in enumerate(block_list):
		if digit == '.':
			# Is there a digit after this position?
			if pos < last_digit_pos:
				# Move digit.
				block_list[pos] = block_list[last_digit_pos]
				block_list[last_digit_pos] = '.'
				# Update last_digit_pos.
				while block_list[last_digit_pos] == '.':
					last_digit_pos -= 1
			else:
				break
			
	return block_list

def calculate_checksum(compressed_block_list):
	checksum = 0
	for pos, digit in enumerate(compressed_block_list):
		if digit != '.':
			checksum += pos * int(digit)

	return checksum

block_list = expand_disk_map1(disk_map)

print(block_list)

block_list = compress_disk_map1(block_list)

# Calculate checksum.

print(f'checksum = {calculate_checksum(block_list)}')

# PART 2

def expand_disk_map2(disk_map):
	# Expand disk_map into block representation. Return block representation, and
	# dict indicating start pos for each file ID.
	id = 0
	block_list = []
	file_start_pos = {}
	for pos, digit in enumerate(disk_map):
		# Even => file, odd => free space.
		if pos % 2 == 0:
			file_start_pos[id] = len(block_list)
			block_list += [id] * digit
			id += 1
		else:
			block_list += ['.'] * digit

	return block_list, file_start_pos

def compress_disk_map2(block_list, file_start_pos):
	last_file_id = max(file_start_pos.keys())

	# Loop through files from end of disk map to beginning.
	for id in range(last_file_id, 0, -1):
		# Determine how many blocks it takes.
		pos = file_start_pos[id]
		while pos < len(block_list) and block_list[pos] == id:
			pos += 1
		file_len = pos - file_start_pos[id]

		# Look for a span of free space that fits the file, from left to right.
		done = False
		pos = 0
		while not done:
			if block_list[pos] == '.':
				# Found free space; determine how long it is.
				start_pos = pos
				while block_list[pos] == '.':
					pos += 1
				# Is span long enough?
				if pos - start_pos >= file_len:
					# Move file.
					block_list[start_pos:start_pos+file_len] = [id] * file_len
					block_list[file_start_pos[id]:file_start_pos[id]+file_len] = '.' * file_len
					done = True
				else:
					pos = start_pos + 1
			else:
				pos += 1

			if pos >= file_start_pos[id]:
				done = True

	return block_list

block_list, file_start_pos = expand_disk_map2(disk_map)

print(block_list)

block_list = compress_disk_map2(block_list, file_start_pos)

# Calculate checksum.

print(f'checksum = {calculate_checksum(block_list)}')




