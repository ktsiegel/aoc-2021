
def main():
	with open('day6_input.txt', 'r') as f:
		fish = [int(x.strip()) for x in f.readline().strip().split(',')]

	for d in range(0,80):
		l = len(fish)
		for i in range(0,l):
			if fish[i] > 0:
				fish[i] = fish[i] - 1
			else:
				fish[i] = 6
				fish.append(8)
	print(fish)
	print len(fish)
	
		
	




if __name__ == "__main__":
	main()
