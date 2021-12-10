import functools

def main():
	with open('day7_input.txt', 'r') as f:
		positions = [int(x.strip()) for x in f.readline().strip().split(',')]

	positions.sort()
	print(positions)

	min_pos = positions[0]
	max_pos = positions[len(positions)-1]
	potential_ends = [0]*(max_pos-min_pos+1)
	for i in range(0, len(potential_ends)):
		for p in positions:
			actual_pos = i+min_pos
			diff = abs(p-actual_pos)
			potential_ends[i] += diff
	print(potential_ends)
	print(functools.reduce(lambda a, b: min(a,b), potential_ends))
	
		


	


if __name__ == "__main__":
	main()
