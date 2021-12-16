from copy import deepcopy

# Perform num_steps steps of the polymerization process,
# inserting characters into input_polymer according to the
# instructions map (maps pairs to the character that should be inserted.
def perform_n_steps(input_polymer, instructions, num_steps):
    polymer = input_polymer
    for step in range(num_steps):
        updated_polymer = polymer[0]
        for i in range(1, len(polymer)):
            # add character between this one and the last one
            updated_polymer += instructions[polymer[i-1:i+1]]
            # add this character
            updated_polymer += polymer[i]
        polymer = updated_polymer
    return polymer

# calculate_score takes the occurrence of the most common letter and subtracts
# the occurrence of the least common letter.
def calculate_score(polymer):
    letter_counts = dict()
    for c in polymer:
        if c in letter_counts.keys():
            letter_counts[c] += 1
        else:
            letter_counts[c] = 1

    min_count = letter_counts[polymer[0]]
    max_count = letter_counts[polymer[0]]
    for l in letter_counts.keys():
        min_count = min(letter_counts[l], min_count)
        max_count = max(letter_counts[l], max_count)
    return max_count - min_count

def get_input(filename):
    with open(filename, 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    polymer = lines[0]
    instructions = dict()
    for i in range(2,len(lines)):
        [pair, inserted_char] = lines[i].split(' -> ')
        instructions[pair] = inserted_char

    return polymer, instructions


def run_test():
    (polymer, instructions) = get_input('example_input.txt')
    assert perform_n_steps(polymer, instructions, 1) == 'NCNBCHB'
    assert perform_n_steps(polymer, instructions, 2) == 'NBCCNBBBCBHCB'
    assert perform_n_steps(polymer, instructions, 3) == 'NBBBCNCCNBBNBNBBCHBHHBCHB'
    assert perform_n_steps(polymer, instructions, 4) == 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'

    ten_step_polymer = perform_n_steps(polymer, instructions, 10)
    assert len(ten_step_polymer) == 3073
    assert calculate_score(ten_step_polymer) == 1588

def run_real_input():
    (polymer, instructions) = get_input('input.txt')
    ten_step_polymer = perform_n_steps(polymer, instructions, 10)
    return calculate_score(ten_step_polymer)

def main():
    run_test()
    print('part 1: {}'.format(run_real_input()))

if __name__ == "__main__":
	main()


