# Read file.
with open('day5/aoc_day5.txt') as f:
	lines = f.read().splitlines() # splitlines gets rid of \n at end of lines

# Split lines into rules and updates.
blank_line = lines.index('')
rules = lines[:blank_line]
updates = lines[blank_line+1:]

# Split rules and updates into constituent parts, and convert to ints.
rules = [r.split('|') for r in rules]
updates = [u.split(',') for u in updates]
rules = [[int(r[n]) for n in range(len(r))] for r in rules]
updates = [[int(u[n]) for n in range(len(u))] for u in updates]

def violated_rule(update):
	# Return violated rule (as 2-list), or None if list is safe.
	for r in rules:
		if r[0] in u and r[1] in u:
			if u.index(r[0]) > u.index(r[1]):
				return r

	return None

# PART 1

# Check updates.
safe_updates = []
unsafe_updates = []
for u in updates:
	if violated_rule(u) is None:
		safe_updates.append(u)
	else:
		unsafe_updates.append(u)

num_safe_updates = len(safe_updates)
sum_of_middles = sum([u[int(len(u)/2)] for u in safe_updates])

print(f'{num_safe_updates} safe updates with middle-sum {sum_of_middles}')

# PART 2

# Strategy (definitely not the most efficient): 
# Find violated rule; move second item to just before first; repeat until safe.
for u in unsafe_updates:
	viol = violated_rule(u)
	while viol is not None:
		# Move second item to just before first.
		p0_index = u.index(viol[0])
		p1_index = u.index(viol[1])
		u.insert(p0_index, u.pop(p1_index))
		# Check again.
		viol = violated_rule(u)

sum_of_middles = sum([u[int(len(u)/2)] for u in unsafe_updates])

print(f'middle-sum of newly safe updates = {sum_of_middles}')
