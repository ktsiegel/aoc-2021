# used for error score calculation
illegal_char_values = {')':3, ']': 57, '}':1197, '>':25137}

# used for autocomplete score calculation
closing_char_values = {')':1, ']':2, '}':3, '>':4}

chunk_open_to_close = {'(':')', '[':']', '{':'}', '<':'>'}

def find_first_illegal_char(nav_line):
    stack = []
    for c in nav_line:
        if c in '([{<': # chunk opens
            stack.append(c)
        else: # chunk closes
            chunk_open = stack.pop(len(stack)-1)
            if chunk_open_to_close[chunk_open] != c:
                # corrupted
                return c, None

    return None, stack

def get_scores(nav_lines):
    error_score = 0
    autocomplete_scores = []
    for nav_line in nav_lines:
        illegal_char, remaining_stack = find_first_illegal_char(nav_line.strip())
        if illegal_char != None:
            error_score += illegal_char_values[illegal_char]
        else:
            autocomplete_scores.append(get_autocomplete_score(remaining_stack))
    autocomplete_scores.sort()
    return error_score, autocomplete_scores[int(len(autocomplete_scores)/2)]

def get_autocomplete_score(remaining_stack):
    score = 0
    for i in range(len(remaining_stack)-1, -1, -1):
        c = remaining_stack[i]
        score *= 5
        score += closing_char_values[chunk_open_to_close[c]]
    return score

def main():
    with open('day10_input.txt', 'r') as f:
        nav_lines = [x.strip() for x in f.readlines()]

    error_score, autocomplete_score = get_scores(nav_lines)
    print('Error Score: {}'.format(error_score))
    print('Autocomplete Score: {}'.format(autocomplete_score))


if __name__ == "__main__":
	main()
