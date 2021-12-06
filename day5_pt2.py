

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
	for i in range(0, max_y+1):
		row = []
		for j in range(0, max_x+1):
			row.append(0)
		graph.append(row)
		
	# print(graph)
	
	for l in lines:
		# print('line {}'.format(l))
		if l[0][0] == l[1][0]:
			## vertical line
			start_y = min(l[0][1], l[1][1])
			end_y = max(l[0][1], l[1][1])
			for r in range(start_y, end_y + 1):
				graph[r][l[0][0]] += 1
		elif l[0][1] == l[1][1]:
			## horizontal line
			start_x = min(l[0][0],l[1][0])
			end_x = max(l[0][0],l[1][0])
			for c in range(start_x, end_x+1):
				graph[l[0][1]][c] += 1
		else:
			# diagonal line
			step_x = 1
			step_y = 1
			start_x = l[0][0]
			end_x = l[1][0]
			start_y = l[0][1]
			end_y = l[1][1]
			if start_x > end_x:
				step_x = -1
			if start_y > end_y:
				step_y = -1
			j = 0
			for x_loc in range(start_x, end_x + step_x, step_x):
				y_loc = start_y + (j*step_y)
				graph[y_loc][x_loc] += 1
				j += 1
	for r in graph:
		print(' '.join([str(x) for x in r]).replace('0','.'))
	
		
	count = 0
	for row in graph:
		for square in row:
			if square > 1:
				count += 1
	print(count)
	




if __name__ == "__main__":
	main()
