from copy import deepcopy

# Perform num_steps steps of the polymerization process,
# inserting characters into input_polymer according to the
# instructions map (maps pairs to the character that should be inserted.
def perform_n_steps(input_polymer, instructions, num_steps):
    # maps adjacent pairs of letters in the current polymer to a count of their
    # occurrence
    pair_counts = dict()
    for i in range(len(input_polymer)-1):
        pair = input_polymer[i:i+2]
        if pair in pair_counts.keys():
            pair_counts[pair] += 1
        else:
            pair_counts[pair] = 1

    for step in range(num_steps):
        updated_pair_counts = dict()
        for pair in pair_counts.keys():
            inserted_letter = instructions[pair]
            new_pairs = [pair[0] + inserted_letter, inserted_letter + pair[1]]
            for p in new_pairs:
                if p in updated_pair_counts.keys():
                    updated_pair_counts[p] += pair_counts[pair]
                else:
                    updated_pair_counts[p] = pair_counts[pair]
        pair_counts = updated_pair_counts
    return pair_counts

def score_n_steps(polymer, instructions, num_steps):
    pair_counts = perform_n_steps(polymer, instructions, num_steps)
    letter_counts = dict()
    for pair in pair_counts.keys():
        for l in pair:
            if l in letter_counts.keys():
                letter_counts[l] += pair_counts[pair]
            else:
                letter_counts[l] = pair_counts[pair]
    # The first and last letter aren't counted double yet, but all other
    # letters are. So, add 1 for the first and last letters, then divide all
    # counts by 2.
    letter_counts[polymer[0]] += 1
    letter_counts[polymer[-1]] += 1

    max_count = letter_counts[polymer[0]]/2
    min_count = letter_counts[polymer[0]]/2
    for l in letter_counts.keys():
        max_count = max(letter_counts[l]/2, max_count)
        min_count = min(letter_counts[l]/2, min_count)
    return int(max_count - min_count)

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
    assert score_n_steps(polymer, instructions, 1) == 1
    assert score_n_steps(polymer, instructions, 2) == 5
    assert score_n_steps(polymer, instructions, 40) == 2188189693529

    (polymer, instructions) = get_input('input.txt')
    print('part 2: {}'.format(score_n_steps(polymer, instructions, 40)))

def main():
    run_test()

if __name__ == "__main__":
	main()


