
def main():
	with open('day3_input.txt', 'r') as f:
		report = [x.strip() for x in f.readlines()]

	## counts contains a tuple for each digit (num 0s, num 1s)
	counts = []
	for i in range(0, len(report[0])):
		counts.append([0,0])
	for num in report:
		print(num)
		for i in range(0, len(num)):
			digit = num[i]
			if digit == '0':
				counts[i][0] += 1
			elif digit == '1':
				counts[i][1] += 1
	print(counts)

	gamma = ''
	epsilon = ''
	for c in counts:
		if c[0] > c[1]:
			gamma += '0'
			epsilon += '1'
		else:
			gamma += '1'
			epsilon += '0'
		
	gamma_base10 = int(gamma,2)
	epsilon_base10 = int(epsilon,2)
	print('{}'.format(gamma_base10))
	print('{}'.format(epsilon_base10))
	print('{}'.format(gamma_base10*epsilon_base10))
		
	




if __name__ == "__main__":
	main()
