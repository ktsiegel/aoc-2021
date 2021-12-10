
def main():
	with open('day6_input.txt', 'r') as f:
		fish = [int(x.strip()) for x in f.readline().strip().split(',')]

	all_fish = [0]*9
	for f in fish:
		all_fish[f] += 1
	
	for d in range(0,256):
		updated = [0]*9
		for i in range(0,8):
			updated[i] = all_fish[i+1]
		updated[6] += all_fish[0]
		updated[8] = all_fish[0]
		all_fish = updated

	print(all_fish)
	count = 0
	for f in all_fish:
		count += f
	print(count)
	
		
	




if __name__ == "__main__":
	main()
