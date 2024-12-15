import itertools
import tqdm

# Read file.
with open('day7/aoc_day7.txt') as f:
	lines = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Parse lines.
test_values = []
equations = []
for l in lines:
	[test_val, eq] = l.split(': ')
	test_values.append(int(test_val))
	equations.append([int(num) for num in eq.split(' ')])

def test_equations(equations):
	pbar = tqdm.tqdm(total=len(equations))
	pbar.display()
	# Determine which equations can be made true. (Just use brute force search over operators.)
	num_true = 0
	sum_test_values = 0
	for m, eq in enumerate(equations):
		pbar.update()
		# Get all combinations of + and *.
		op_combins = list(itertools.product(OPERATORS, repeat=len(eq) - 1))
		# Always start with +. (This just adds the first result to 0.)
		op_combins_with_plus = []
		for op_combin in op_combins:
			op_combins_with_plus.append(['+'] + [op for op in op_combin])
		# Loop through operation combinations.
		for op_combin in op_combins_with_plus:
			result = 0
			for n in range(len(eq)):
				if op_combin[n] == '+':
					result += eq[n]
				elif op_combin[n] == '*':
					result *= eq[n]
				elif op_combin[n] == '||':
					result = int(str(result) + str(eq[n]))
			# Compare to test value.
			if result == test_values[m]:
				num_true += 1
				sum_test_values += test_values[m]
				break

	return num_true, sum_test_values

# PART 1

OPERATORS = ('+', '*')

num_true, sum_test_values = test_equations(equations)

print(f'part 1: number of equations that can be made true = {num_true}; sum of test values = {sum_test_values}')

# PART 2

OPERATORS = ('+', '*', '||')

num_true, sum_test_values = test_equations(equations)

print(f'part 2: number of equations that can be made true = {num_true}; sum of test values = {sum_test_values}')


