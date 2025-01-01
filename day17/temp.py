import re

# copied from https://github.com/mgtezak/Advent_of_Code/blob/master/2024/17/p2.py


def part2(register, program):
#    register, program = puzzle_input.split('\n\n')
    # _, B, C = map(int, re.findall(r'\d+', register))
    # program = [int(i) for i in re.findall(r'\d+', program)]
    B, C = register['B'], register['C']
    n = len(program)

    def run_program(A):

        def combo(operand):
            if operand == 4:
                return register['A']
            if operand == 5:
                return register['B']
            if operand == 6:
                return register['C']
            return operand
        
        register = dict(A=A, B=B, C=C)
        i = 0
        out = []
        while i < n:
            opcode, operand = program[i:i+2]
            match opcode:
                case 0:
                    register['A'] >>= combo(operand)
                case 1:
                    register['B'] ^= operand
                case 2:
                    register['B'] = combo(operand) % 8
                case 3:
                    if register['A']:
                        i = operand - 2
                case 4:
                    register['B'] ^= register['C']
                case 5:
                    out.append(combo(operand) % 8)
                case 6:
                    register['B'] = register['A'] >> combo(operand)
                case 7:
                    register['C'] = register['A'] >> combo(operand)
            i += 2
            
        return out
    
    A = 0
    for i in reversed(range(n)):
        A <<= 3
        while run_program(A) != program[i:]:
            A += 1

    return A


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

if __name__ == "__main__":
    # start_time = time.time()
    # result = solve_aoc()
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    register, program = read_data()
    result = part2(register, program)
    print(f"Result: {result}")
#    print(f"Elapsed time: {elapsed_time:.6f} seconds")