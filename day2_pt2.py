
def main():
	with open('day2_input.txt', 'r') as f:
		instructions = [x.strip() for x in f.readlines()]
	print(instructions)
	horizontal_pos = 0
	depth = 0
	aim = 0
	for instruction in instructions:
		[direction, steps_str] = instruction.split(" ")
		steps = int(steps_str)
		if direction == "forward":
			horizontal_pos += steps
			depth += aim * steps
		elif direction == "down":
			aim += steps
		elif direction == "up":
			aim -= steps
	print('{}'.format(horizontal_pos))
	print('{}'.format(depth))
	print('{}'.format(horizontal_pos * depth))

	
		
	




if __name__ == "__main__":
	main()
