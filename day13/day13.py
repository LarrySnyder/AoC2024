import functools
import numpy as np


# Read file.
with open('day13/aoc_day13.txt') as f:
	input = f.read().splitlines() # splitlines gets rid of \n at end of lines

A_COST = 3
B_COST = 1

PART = 2

class Machine:
	def __init__(self, AX, AY, BX, BY, PX, PY):
		self.AX = AX
		self.AY = AY
		self.BX = BX
		self.BY = BY
		self.PX = PX
		self.PY = PY


# Parse input.
machines = []
done = False
row = 0
while not done:
	AX_start = np.int64(input[row].find('X+'))
	AX_end = np.int64(input[row].find(','))
	AY_start = np.int64(input[row].find('Y+'))
	AX = np.int64(input[row][AX_start+2:AX_end])
	AY = np.int64(input[row][AY_start+2:])

	BX_start = np.int64(input[row+1].find('X+'))
	BX_end = np.int64(input[row+1].find(','))
	BY_start = np.int64(input[row+1].find('Y+'))
	BX = np.int64(input[row+1][BX_start+2:BX_end])
	BY = np.int64(input[row+1][BY_start+2:])

	PX_start = np.int64(input[row+2].find('X='))
	PX_end = np.int64(input[row+2].find(','))
	PY_start = np.int64(input[row+2].find('Y='))
	PX = np.int64(input[row+2][PX_start+2:PX_end])
	PY = np.int64(input[row+2][PY_start+2:])

	machines.append(Machine(AX, AY, BX, BY, PX, PY))

	row += 4
	if row >= len(input):
		done = True


# PART 1:

@functools.lru_cache(maxsize=None)
def machine_DP(loc, machine):
	if loc == (machine.PX, machine.PY):
		return 0
	elif loc[0] > machine.PX or loc[1] > machine.PY:
		return 1.0e100
	else:
		loc_A = (loc[0] + machine.AX, loc[1] + machine.AY)
		loc_B = (loc[0] + machine.BX, loc[1] + machine.BY)
		return min(A_COST + machine_DP(loc_A, machine), B_COST + machine_DP(loc_B, machine))
	
	
if PART == 1:
	import sys
	sys.setrecursionlimit(2000)

	total_tokens = 0
	for m_ind, machine in enumerate(machines):
		opt_cost = machine_DP((0, 0), machine)
		if opt_cost < 1.0e99:
			total_tokens += opt_cost
		print(f'Machine {m_ind+1}: optimal cost = {opt_cost}')
		
	print(f'Total tokens = {total_tokens}')


# PART 2
# min A_COST * n_A + B_COST * n_B -- actually it's 2 equations 2 unknowns so no need to optimize
# s.t.  n_A * AX + n_B * BX = PX
# 		n_A * AY + n_B * BY = PY

else:

	# Update P.
	for machine in machines:
		machine.PX += 10000000000000
		machine.PY += 10000000000000

	total_tokens = 0
	for m_ind, m in enumerate(machines):

		# coeff_matrix = np.array([[m.AX, m.BX], [m.AY, m.BY]])
		# rhs = np.array([m.PX, m.PY])
		# n_A, n_B = np.linalg.solve(coeff_matrix, rhs)

		# Cramer's rule.
		D = m.AX * m.BY - m.BX * m.AY
		D_A = m.PX * m.BY - m.BX * m.PY
		D_B = m.AX * m.PY - m.PX * m.AY

		n_A = D_A / D
		n_B = D_B / D

		if n_A != int(n_A) or n_B != int(n_B):
			print(f'Machine {m_ind+1}: not integer')
		else:
			tokens = A_COST * n_A + B_COST * n_B
			print(f'Machine {m_ind+1}: cost = {tokens}')
			total_tokens += tokens

		# env = gp.Env(empty=True)
		# env.setParam('OutputFlag', 0)
		# env.start()

		# # Create model.
		# model = gp.Model('claw', env=env)

		# # Create variables.
		# n_A = model.addVar(vtype=GRB.CONTINUOUS, name='n_A')
		# n_B = model.addVar(vtype=GRB.CONTINUOUS, name='n_B')

		# # Set objective.
		# model.setObjective(A_COST * n_A + B_COST * n_B, GRB.MINIMIZE)

		# # Add constraints.
		# model.addConstr(n_A * machine.AX + n_B * machine.BX == machine.PX, "c_X")
		# model.addConstr(n_A * machine.AY + n_B * machine.BY == machine.PY, "c_Y")

		# # Optimize.
		# model.optimize()

		# if model.Status == GRB.INFEASIBLE:
		# 	print(f'Machine {m+1}: infeasible')
		# # Check integrality. (Setting vtype = INTEGER didn't work for some reason.)
		# elif n_A.X != int(n_A.X) or n_B.X != int(n_B.X):
		# 	print(f'Machine {m+1}: not integer')
		# else:
		# 	print(f'Machine {m+1}: optimal cost = {model.ObjVal}, n_A = {n_A.X}, n_B = {n_B.X}')
		# 	total_tokens += model.ObjVal
		
	print(f'Total tokens = {total_tokens}')
