

def main():
	with open('day5_input.txt', 'r') as f:
		raw_lines = [x.strip().split(' -> ') for x in f.readlines()]

	lines = []
	max_x = 0
	max_y = 1
	for l in raw_lines:
		line = [[int(x) for x in l[0].split(',')], [int(x) for x in l[1].split(',')]]
		lines.append(line)
		max_x = max(max_x,line[0][0])
		max_x = max(max_x,line[1][0])
		max_y = max(max_y,line[0][1])
		max_y = max(max_y,line[1][1])
	# print(lines)
	# print(max_x)
	# print(max_y)
	
	graph = []
	for i in range(0, max_x+1):
		row = []
		for j in range(0, max_y+1):
			row.append(0)
		graph.append(row)
		
	# print(graph)
	
	for l in lines:
		# only check horizontal or vertical
		# print('line {}'.format(l))
		if l[0][0] == l[1][0]:
			## vertical line
			start_y = min(l[0][1], l[1][1])
			end_y = max(l[0][1], l[1][1])
			for r in range(start_y, end_y + 1):
				graph[l[0][0]][r] += 1
		if l[0][1] == l[1][1]:
			## horizontal line
			start_x = min(l[0][0],l[1][0])
			end_x = max(l[0][0],l[1][0])
			for c in range(start_x, end_x+1):
				graph[c][l[0][1]] += 1
	for r in graph:
		print(r)
	
		
	count = 0
	for row in graph:
		for square in row:
			if square > 1:
				count += 1
	print(count)
	




if __name__ == "__main__":
	main()
