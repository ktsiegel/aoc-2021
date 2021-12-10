import functools

		
def get_digits(code_str):
	[all_digits_raw, code_raw] = code_str.split('|')
	all_digits = all_digits_raw.strip().split(' ')
	code = code_raw.strip().split(' ')
	print(all_digits)
	print(code)

	five_digits = [] # two, three, five, 
	six_digits = [] # zero, six, nine
	for d in all_digits:
		if len(d) == 2:
			one = d
		if len(d) == 3:
			seven = d
		if len(d) == 4:
			four = d
		if len(d) == 5:
			five_digits.append(d)
		if len(d) == 6:
			six_digits.append(d)
		if len(d) == 7:
			eight = d
	
	possible = [] # x by y array where it's true if x can map to y, where y is the pos in properly formed diagram and x is the mixed signal
	for i in range(0,7):
		poss_row = [True] * 7
		possible.append(poss_row)

	indices = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}
	reverse_indices = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g'}

	for letter in one:
		# each character can map to 'c' or 'f', and not anything else
		for i in range(0,7):
			if reverse_indices[i] != 'c' and reverse_indices[i] != 'f':
				possible[indices[letter]][i] = False

	for letter in seven:
		# each character can map to a, c, or f, and not anything else
		for i in range(0,7):
			if reverse_indices[i] != 'c' and reverse_indices[i] != 'f' and reverse_indices[i] != 'a':
				possible[indices[letter]][i] = False

	for letter in four:
		# each character can map to b, c, d, or f, and not anything else
		for i in range(0,7):
			if reverse_indices[i] != 'b' and reverse_indices[i] != 'c' and reverse_indices[i] != 'd' and reverse_indices[i] != 'f':
				possible[indices[letter]][i] = False

	# of the 5 digit ones, they will share 3 connections, and two will differ
	five_conns = [0] * 7 # map letter to count
	for digit in five_digits:
		for letter in digit:
			five_conns[indices[letter]] += 1

	for conn_idx in range(0, len(five_conns)):
		if five_conns[conn_idx] == 3:
			# a, d, or g, and not anything else
			for i in range(0,7):
				if reverse_indices[i] != 'a' and reverse_indices[i] != 'd' and reverse_indices[i] != 'g':
					possible[conn_idx][i] = False
		if five_conns[conn_idx] == 2:
			# c or f
			for i in range(0, 7):
				if reverse_indices[i] != 'c' and reverse_indices[i] != 'f':
					possible[conn_idx][i] = False
		if five_conns[conn_idx] == 1:
			# b or e
			for i in range(0,7):
				if reverse_indices[i] != 'b' and reverse_indices[i] != 'e':
					possible[conn_idx][i] = False

	# 6 digit numbers
	six_conns = [0] * 7
	for digit in six_digits:
		for letter in digit:
			six_conns[indices[letter]] += 1
	
	for conn_idx in range(0, len(six_conns)):
		if six_conns[conn_idx] == 3:
			# abfg
			possible[conn_idx][indices['c']] = False
			possible[conn_idx][indices['d']] = False
			possible[conn_idx][indices['e']] = False
		if six_conns[conn_idx] == 2:
			# cde
			possible[conn_idx][indices['a']] = False
			possible[conn_idx][indices['b']] = False
			possible[conn_idx][indices['f']] = False
			possible[conn_idx][indices['g']] = False


	for p in possible:
		print(p)

	# generate final letter mapping
	mappings = dict()
	for row in range(0, len(possible)):
		# row is the pre-mapped letter
		letter = -1
		for j in range(0, len(possible[row])):
			if possible[row][j] == True:
				letter = j
		mappings[reverse_indices[row]] = reverse_indices[letter]

	print(mappings)

	real_digit_mapping = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

	decoded = ''
	for c in code:
		converted_letters = ''
		for letter in c:
			converted_letter = mappings[letter]
			converted_letters += converted_letter
		print(converted_letters)
		index = str(real_digit_mapping.index(''.join(sorted(converted_letters))))
		decoded += index
	print(decoded)
	return int(decoded)


def test():
	assert get_digits('be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe') == 8394
	assert get_digits('edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc') == 9781
	assert get_digits('fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg') == 1197
	assert get_digits('fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb') == 9361
	assert get_digits('aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea') == 4873
	assert get_digits('fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb') == 8418
	assert get_digits('dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe') == 4548
	assert get_digits('bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef') == 1625
	assert get_digits('egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb') == 8717
	assert get_digits('gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce') == 4315
	

def main():
	with open('day8_input.txt', 'r') as f:
		lines = f.readlines()

	c = 0
	for l in lines:
		c += get_digits(l.strip())
		# [digits, code] = l.split('|')
		# code_digits = code.strip().split(' ')
		# for d in code_digits:
			# if len(d) <= 4 or len(d) == 7:
				# c += 1

	print(c)



if __name__ == "__main__":
	# test()
	main()
