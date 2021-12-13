from copy import deepcopy

def find_paths(cave_map):
    path_list = []
    queue = [['start']]
    while len(queue) > 0:
        cur_path = queue.pop(0)
        for dest in cave_map[cur_path[-1]]:
            if dest in cur_path and dest.islower():
                continue
            new_path = deepcopy(cur_path)
            new_path.append(dest)
            if dest == 'end':
                path_list.append(new_path)
            else:
                queue.append(new_path)
    return path_list


def main():
    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    # maps path start to a list of possible path ends for a single leg
    # if 'b' is in the list that 'a' maps to, 'a' will be in the list 'b' maps
    # to.
    cave_map = dict()
    for l in lines:
        [start, end] = l.strip().split('-')
        if start in cave_map.keys():
            cave_map[start].append(end)
        else:
            cave_map[start] = [end]
        if end in cave_map.keys():
            cave_map[end].append(start)
        else:
            cave_map[end] = [start]
    print(cave_map)

    paths = find_paths(cave_map)
    for p in paths:
        print(','.join(p))
    print(len(paths))

if __name__ == "__main__":
	main()
