from copy import deepcopy

def print_herd(herd):
    for line in herd:
        print(''.join(line))
    print('')

def solve(lines):
    herd = []
    for line in lines:
        herd.append([c for c in line])
    # print_herd(herd)
    i = 1
    while True:
        changes = 0
        new_herd = deepcopy(herd)
        # first move east cucumbers
        for row in range(len(herd)):
            for col in range(len(herd[0])):
                if herd[row][col] == '>':
                    dest_col = (col + 1) % len(herd[0])
                    if herd[row][dest_col] == '.':
                        # moves east
                        new_herd[row][col] = '.'
                        new_herd[row][dest_col] = '>'
                        changes += 1
        herd = new_herd
        new_herd = deepcopy(herd)
        # then move south cucumbers
        for row in range(len(herd)):
            for col in range(len(herd[0])):
                if herd[row][col] == 'v':
                    dest_row = (row + 1) % len(herd)
                    if herd[dest_row][col] == '.':
                        # moves south
                        new_herd[row][col] = '.'
                        new_herd[dest_row][col] = 'v'
                        changes += 1
        if changes == 0:
            return i
        i += 1
        herd = new_herd


def main():
    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    print(solve(lines))


if __name__ == "__main__":
	main()
