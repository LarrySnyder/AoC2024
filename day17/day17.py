import time

PART = 2
SAMPLE = False
if SAMPLE:
	FILENAME = 'day17/aoc_day17_sample.txt'
else:
	FILENAME = 'day17/aoc_day17.txt'

def read_data():
	with open(FILENAME) as f:
		info = f.read().splitlines() # splitlines gets rid of \n at end of lines
	
	registers = {
		'A': int(info[0][12:]),
		'B': int(info[1][12:]),
		'C': int(info[2][12:])
	}

	program = list(info[4][9:].split(','))
	program = [int(p) for p in program]

	return registers, program

def combo_operand(operand, registers):
	if 0 <= operand <= 3:
		return operand
	elif operand == 4:
		return registers['A']
	elif operand == 5:
		return registers['B']
	elif operand == 6:
		return registers['C']
	elif operand == 7:
		return None

def run_program(registers, program):
	# Initialize instruction pointer.
	ip = 0

	# Initialize output.
	output = []

	while ip < len(program):
		# Read opcode and operand.
		opcode = program[ip]
		operand = program[ip+1]

		# Flag to indicate whether we jumped.
		jumped = False

		# Determine operation.
		match opcode:
			case 0:
				# adv
				result = int(registers['A'] / (2 ** combo_operand(operand, registers)))
				registers['A'] = result
			case 1:
				# bxl
				# (python ^ operator is bitwise XOR; it accepts decimals and returns a decimal but
				# is oprating on the binary representations)
				result = registers['B'] ^ operand
				registers['B'] = result
			case 2:
				# bst
				result = combo_operand(operand, registers) % 8
				registers['B'] = result
			case 3:
				# jnz
				if registers['A'] != 0:
					ip = operand
					jumped = True
			case 4:
				# bxc
				result = registers['B'] ^ registers['C']
				registers['B'] = result
			case 5:
				# out
				result = combo_operand(operand, registers) % 8
				output.append(result)
			case 6:
				# bdv
				result = int(registers['A'] / (2 ** combo_operand(operand, registers)))
				registers['B'] = result
			case 7:
				# cdv
				result = int(registers['A'] / (2 ** combo_operand(operand, registers)))
				registers['C'] = result

		# Update ip.
		if not jumped:
			ip += 2
	
	return registers, ','.join([str(i) for i in output])
	
def find_fixed_point(registers, program):
	# COULDN"T SOLVE THIS -- WOUND UP GIVING UP AND USING CODE IN TEMP.PY
	a = 0
	while True:
		if a % 10000 == 0:
			print(f'a = {a}')
		registers['A'] = a
		result = run_program(registers, program)
		if result[1] == ','.join([str(i) for i in program]):
			break
		a += 1

	return a

def solve_aoc():
	registers, program = read_data()
	if PART == 1:
		result = run_program(registers, program)
	else:
		result = find_fixed_point(registers, program)
	return result


if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")