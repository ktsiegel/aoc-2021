
# returns a copy of the boards, updated to their state after 'draw' is drawn and applied
def update_boards(boards, draw):
	updated = []
	for b in boards:
		updated_board = []
		for b_line in b:
			updated_line = []
			for b_square in b_line:
				drawn = b_square[1]
				if draw == b_square[0]:
					drawn = True
				updated_line.append([b_square[0], drawn])
			updated_board.append(updated_line)
		updated.append(updated_board)
	return updated

# returns the index of the bingo board if a bingo is found.
# otherwise returns -1 if no board has a bingo
def check_bingo(boards):
	for b_index in range(0, len(boards)):
		b = boards[b_index]
		# check rows for bingos
		for r in range(0, len(b)):
			is_bingo = True
			for c in range(0, len(b[0])):
				if b[r][c][1] == False:
					is_bingo = False
					break
			if is_bingo:
				# found a row bingo!
				print('row')
				return b_index
		# check columns for bingos
		for c in range(0, len(b[0])):
			is_bingo = True
			for r in range(0, len(b)):
				if b[r][c][1] == False:
					is_bingo = False
					break
			if is_bingo:
				# found a column bingo!
				print('col')
				return b_index
	return -1


def calculate_sum_not_called(board):
	c = 0
	for b_row in board:
		for b_square in b_row:
			if b_square[1] == False:
				c += b_square[0]
	return c

def main():
	with open('day4_input.txt', 'r') as f:
		draws = [int(x) for x in f.readline().strip().split(',')]
		
		# each board in boards is a 5x5x2 array. The 5x5 represents the board,
		# and the 3rd dimension represents [value, whether the value was called yet]
		boards = []
		cur_board = []
		for l in f.readlines():
			board_row = [[int(x),False] for x in l.strip().split(' ') if len(x) > 0]
			if len(board_row) == 5:
				## skip bad/empty rows
				cur_board.append(board_row)
			if len(cur_board) == 5:
				boards.append(cur_board)
				cur_board = []
	print(draws)
	print(boards)

	for draw in draws:
		print(draw)
		boards = update_boards(boards, draw)
		# print(boards)
		winning_bingo_board = check_bingo(boards)
		# print(winning_bingo_board)
		while winning_bingo_board != -1:
			if len(boards) > 1:
				print(winning_bingo_board)
				print(boards.pop(winning_bingo_board))
				winning_bingo_board = check_bingo(boards)
			else:
				print(calculate_sum_not_called(boards[winning_bingo_board]) * draw)
				return

		
		
		
	
		
	




if __name__ == "__main__":
	main()
