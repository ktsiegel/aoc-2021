from copy import deepcopy

# topo_map is a n by m map of the heights of the ground in the caves
# does bfs starting at location (i,j) to find basin size, where a basin's
# boundaries are defined by locations of height 9
# returns a tuple representing the new topological map, with searched
# indices marked as -1, and the basin size.
def find_basin_size(topo_map, i, j):
    # clone topo_map
    search_map = deepcopy(topo_map)

    queue = [(i,j)]
    size = 0
    while len(queue) > 0:
        # pop first item
        search_i, search_j = queue.pop(0)
        # check if already searched. if not, add to count and add neighbors to
        # queue
        if search_map[search_i][search_j] != -1 and search_map[search_i][search_j] != 9:
            size += 1
            # only add neighbor if it exists and is not of height 9
            if search_i > 0:
                queue.append((search_i-1, search_j))
            if search_j > 0:
                queue.append((search_i, search_j-1))
            if search_i < len(search_map)-1:
                queue.append((search_i+1, search_j))
            if search_j < len(search_map[0])-1:
                queue.append((search_i, search_j+1))

            # mark as visited
            search_map[search_i][search_j] = -1

    return (search_map, size)


def main():
    with open('day9_input.txt', 'r') as f:
        raw_rows = f.readlines()

    topo_map = []
    for raw_row in raw_rows:
        topo_map.append([int(x) for x in raw_row.strip()])

    print(topo_map)

    basin_sizes = []

    # For every square that is not height 9, do BFS to find the total size of
    # the basin, marking a square as -1 if it is visited.
    for i in range(len(topo_map)):
        for j in range(len(topo_map[0])):
            if topo_map[i][j] != -1:
                updated_topo_map, basin_size = find_basin_size(topo_map, i, j)
                basin_sizes.append(basin_size)

                # update topo map so that we don't double search certain basins
                topo_map = updated_topo_map


    # Find three largest basins
    basin_sizes.sort()

    # Answer:
    print(basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])



if __name__ == "__main__":
    main()
