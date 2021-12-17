import heapq as hq

def get_min_risk(r1, r2):
    if r1 is None and r2 is None:
        return None
    if r1 is None:
        return r2
    if r2 is None:
        return r1
    return min(r1, r2)

def find_lowest_risk_path(grid):
    # At each index, contains the risk of the lowest risk path used to reach
    # that index. If no path has been found yet, then None is present
    memoized_grid = []
    for i in range(len(grid)):
        row = [None] * len(grid[0])
        memoized_grid.append(row)

    memoized_grid[0][0] = 0 # start
    had_updates = True
    while had_updates:
        had_updates = False
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                # find min surrounding risk that is not None
                min_risk = None
                if r > 0:
                    min_risk = get_min_risk(min_risk, memoized_grid[r-1][c])
                if c > 0:
                    min_risk = get_min_risk(min_risk, memoized_grid[r][c-1])
                if r < len(memoized_grid)-1:
                    min_risk = get_min_risk(min_risk, memoized_grid[r+1][c])
                if c < len(memoized_grid[0])-1:
                    min_risk = get_min_risk(min_risk, memoized_grid[r][c+1])
                if min_risk is not None:
                    old_value = memoized_grid[r][c]
                    # update memoized grid
                    memoized_grid[r][c] = get_min_risk(min_risk + grid[r][c],memoized_grid[r][c])
                    if old_value != memoized_grid[r][c]:
                        had_updates = True
        # for r in memoized_grid:
            # print('\t'.join([str(x) for x in r]))
        # print(' ')
    return memoized_grid[len(grid)-1][len(grid[0])-1]

def main():
    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    grid = []
    for l in lines:
        grid.append([int(x) for x in l])

    print(find_lowest_risk_path(grid))

if __name__ == "__main__":
	main()
