
def main():
	with open('day2_input.txt', 'r') as f:
		instructions = [x.strip() for x in f.readlines()]
	print(instructions)
	horizontal_pos = 0
	depth = 0
	for instruction in instructions:
		[direction, steps_str] = instruction.split(" ")
		steps = int(steps_str)
		if direction == "forward":
			horizontal_pos += steps
		elif direction == "down":
			depth += steps
		elif direction == "up":
			depth -= steps
	print('{}'.format(horizontal_pos))
	print('{}'.format(depth))
	print('{}'.format(horizontal_pos * depth))

	
		
	




if __name__ == "__main__":
	main()
