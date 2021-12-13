from copy import deepcopy

num_steps = 100

# Models a single "step" in the octopus problem.
# Returns the updated state of the octopi and the number of flashes during this
# single step.
def model_step(prev_octopi):
    octopi = deepcopy(prev_octopi)
    num_flashes = 0

    # increment all octopi by 1
    for i in range(len(octopi)):
        for j in range(len(octopi[0])):
            octopi[i][j] += 1

    # process flashes
    while True:
        prev_num_flashes = num_flashes
        for i in range(len(octopi)):
            for j in range(len(octopi[0])):
                # if octopus is > 9, then it flashes and gets marked as 0 to
                # indicate that it has flashed (and cannot flash again)
                if octopi[i][j] > 9:
                    num_flashes += 1
                    octopi[i][j] = 0
                    for adjacent_i in range(i-1, i+2):
                        for adjacent_j in range(j-1, j+2):
                            if adjacent_i >= 0 and adjacent_i < len(octopi) and \
                            adjacent_j >= 0 and adjacent_j < len(octopi[0]) and \
                            octopi[adjacent_i][adjacent_j] != 0:
                                octopi[adjacent_i][adjacent_j] += 1

        if prev_num_flashes == num_flashes:
            # no octopi were updated on this round, so break
            break

    return octopi, num_flashes



def main():
    with open('day11_input.txt', 'r') as f:
        octopi = [[int(y) for y in x.strip()] for x in f.readlines()]

    total_flashes = 0
    for i in range(num_steps):
        octopi, num_flashes = model_step(octopi)
        total_flashes += num_flashes

    for row in octopi:
        print(row)
    print(total_flashes)

if __name__ == "__main__":
	main()
