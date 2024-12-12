def next_digits(the_str, max_dig=None):
	# Return first substring of 'the_str' consisting of all digits, up to 'max_dig' digits.
	# Return None if first character is not a digit.
	end_pos = 1
	while the_str[0:end_pos].isdigit() and end_pos <= (max_dig or 10000000):
		end_pos += 1
	end_pos -= 1

	return None if end_pos == 0 else int(the_str[0:end_pos])

# PART 1

# Read file.
with open('day3/aoc_day3.txt') as f:
	corrupted_memory = f.read()

# Parse memory.
done = False
pos = 0
running_sum = 0
while not done:
	# Find next position of 'mul('
	pos = corrupted_memory.find('mul(', pos)
	if pos == -1:
		done = True
	else:
		# Check whether next character(s) are digits.
		pos += 4
		num1 = next_digits(corrupted_memory[pos:], 3)
		if num1 is None:
			continue

		# Check whether next character is comma.
		pos += len(str(num1))
		if corrupted_memory[pos] != ',':
			continue

		# Check whether next character(s) are digits.
		pos += 1
		num2 = next_digits(corrupted_memory[pos:], 3)
		if num2 is None:
			continue

		# Check whether next character is ')'.
		pos += len(str(num2))
		if corrupted_memory[pos] != ')':
			continue

		# Calculate product.
		running_sum += num1 * num2

print(f'sum of products = {running_sum}')

# PART 2

# Read file.
with open('day3/aoc_day3.txt') as f:
	corrupted_memory = f.read()

# Parse memory.
done = False
pos = 0
running_sum = 0
while not done:
	# Find locations of next 'mul(', 'do()', and 'don't()'.
	next_mul = corrupted_memory.find('mul(', pos)
#	next_do = corrupted_memory.find('do()', pos)
	next_dont = corrupted_memory.find("don't()", pos)

	# # If we're in dont_mode, skip to next do().
	# if dont_mode:
	# 	pos = next_do
	# 	dont_mode = False
	# else:
	# We're not in dont_mode. 
	
	# Which is next: mul( or dont()?
	# if next_mul < next_dont:
	# 	# Go to next_mult.
	# 	pos = next_mul

	# If there's a dont() before the next mul(, handle it.
	if next_dont < next_mul:
		# Go to next do() *after* next_dont.
		pos = corrupted_memory.find('do()', next_dont)

	# Find next position of 'mul('
	pos = corrupted_memory.find('mul(', pos)
	if pos == -1:
		done = True
	else:
		# Check whether next character(s) are digits.
		pos += 4
		num1 = next_digits(corrupted_memory[pos:], 3)
		if num1 is None:
			continue

		# Check whether next character is comma.
		pos += len(str(num1))
		if corrupted_memory[pos] != ',':
			continue

		# Check whether next character(s) are digits.
		pos += 1
		num2 = next_digits(corrupted_memory[pos:], 3)
		if num2 is None:
			continue

		# Check whether next character is ')'.
		pos += len(str(num2))
		if corrupted_memory[pos] != ')':
			continue

		# Calculate product.
		running_sum += num1 * num2

print(f'sum of products with conditionals = {running_sum}')
