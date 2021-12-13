
def main():
	with open('day9_input.txt', 'r') as f:
		raw_rows = f.readlines()

	rows = []
	for raw_row in raw_rows:
		rows.append([int(x) for x in raw_row.strip()])

	print(rows)

	count = 0
	for r in range(0, len(rows)):
		for c in range(0, len(rows[0])):
			is_low_point = True
			curr = rows[r][c]
			# top
			if r > 0:
				if rows[r-1][c] <= curr:
					is_low_point = False
			# left
			if c > 0:
				if rows[r][c-1] <= curr:
					is_low_point = False
			# right
			if c < len(rows[0])-1:
				if rows[r][c+1] <= curr:
					is_low_point = False
			# bottom
			if r < len(rows) - 1:
				if rows[r+1][c] <= curr:
					is_low_point = False
			if is_low_point:
				count += curr + 1

	print(count)
	
	




if __name__ == "__main__":
	main()
