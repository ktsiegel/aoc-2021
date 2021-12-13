
def gen_counts(report):
	## counts contains a tuple for each digit (num 0s, num 1s)
	num_digits = len(report[0])
	counts = []
	for i in range(0, num_digits):
		counts.append([0,0])
	for num in report:
		for i in range(0, len(num)):
			digit = num[i]
			if digit == '0':
				counts[i][0] += 1
			elif digit == '1':
				counts[i][1] += 1
	return counts
	

def main():
	with open('day3_input.txt', 'r') as f:
		report = [x.strip() for x in f.readlines()]


	oxygen = [x for x in report]
	co2 = [x for x in report]

	oxygen_i = 0
	while len(oxygen) > 1 and oxygen_i < len(report[0]):
		counts = gen_counts(oxygen)
		print(counts)
		if counts[oxygen_i][0] > counts[oxygen_i][1]:
			oxygen = [x for x in oxygen if x[oxygen_i] == '0']
		else:
			oxygen = [x for x in oxygen if x[oxygen_i] == '1']
		oxygen_i+=1
	print(oxygen)
		
	co2_i = 0
	while len(co2) > 1 and co2_i < len(report[0]):
		counts = gen_counts(co2)
		print(counts)
		if counts[co2_i][0] <= counts[co2_i][1]:
			co2 = [x for x in co2 if x[co2_i] == '0']
		else:
			co2 = [x for x in co2 if x[co2_i] == '1']
		co2_i+=1
	print(co2)
		
	print('{}'.format(int(oxygen[0],2)*int(co2[0],2)))
	




if __name__ == "__main__":
	main()
