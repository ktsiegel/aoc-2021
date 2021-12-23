from copy import deepcopy
import time

# each step is represented as a tuple: (on/off, coordinate bounds)
def parse_step(step):
    (setting, coords_str) = step.strip().split(' ')
    assert setting == 'on' or setting == 'off'
    coord_bounds = [[int(x) for x in coords[2:].split('..')] for coords in coords_str.split(',')]
    return setting, coord_bounds

# a and b are cubes represented by [[xmin, xmax], [ymin, ymax], [zmin, zmax]
def get_overlap(a, b):
    # a range overlaps if the min of the maxes >= the max of the mins
    x_overlap = [max(a[0][0], b[0][0]), min(a[0][1], b[0][1])]
    y_overlap = [max(a[1][0], b[1][0]), min(a[1][1], b[1][1])]
    z_overlap = [max(a[2][0], b[2][0]), min(a[2][1], b[2][1])]
    if x_overlap[0] > x_overlap[1] or y_overlap[0] > y_overlap[1] or z_overlap[0] > z_overlap[1]:
        return None
    return [x_overlap, y_overlap, z_overlap]

def subtract_overlap(old_cube, overlap):
    new_cubes = []
    cube = deepcopy(old_cube)
    for i in range(0, 3):
        # i = 0 -> x, 1 -> y, 2 -> z
        # slice into chunks based on x, y, or z overlap. add the chunks not containing the overlap to new_cubes.
        if cube[i][1] > overlap[i][1]:
            new_cube = deepcopy(cube)
            new_cube[i] = [overlap[i][1] + 1, cube[i][1]]
            new_cubes.append(new_cube)
            # update cube bounds to not include the chunk that we sliced away
            cube[i][1] = overlap[i][1]
        if cube[i][0] < overlap[i][0]:
            new_cube = deepcopy(cube)
            new_cube[i] = [cube[i][0], overlap[i][0] - 1]
            new_cubes.append(new_cube)
            # update cube bounds to not include the chunk that we sliced away
            cube[i][0] = overlap[i][0]
    return new_cubes

def count_cube_volumes(cubes):
    count = 0
    for cube in cubes:
        count += (cube[0][1]-cube[0][0]+1) * (cube[1][1]-cube[1][0]+1) * (cube[2][1]-cube[2][0]+1)
    return count

# curr on is an array of bounds representing non-overlapping cubes in the reactor space
def apply_step(prev, step):
    curr_on = []
    for cube in prev:
        # if the cube overlaps with the bounds in step, break up that cube into 3 cubes,
        # which together represent the volume that doesn't overlap with the bounds in 'step'
        overlap = get_overlap(cube, step[1])
        if overlap is None:
            curr_on.append(cube)
        else:
            new_cubes = subtract_overlap(cube, overlap)
            for c in new_cubes:
                curr_on.append(c)
            assert count_cube_volumes([cube]) - count_cube_volumes([overlap]) == count_cube_volumes(new_cubes)
    # append the new cube area, if the step represents turning an area "on"
    if step[0] == 'on':
        curr_on.append(step[1])
    return curr_on

def solve(input_lines):
    steps = [parse_step(step) for step in input_lines]
    i = 0
    while steps[i][0] != 'on':
        i += 1
    curr_on = [steps[i][1]]
    i += 1
    while i < len(steps):
        curr_on = apply_step(curr_on, steps[i])
        i += 1
    return count_cube_volumes(curr_on)

def main():
    assert solve(['on x=10..12,y=10..12,z=10..12']) == 27
    assert solve(['on x=10..12,y=10..12,z=10..12','on x=11..13,y=11..13,z=11..13']) == 46
    assert solve(['on x=10..12,y=10..12,z=10..12','on x=11..13,y=11..13,z=11..13','off x=9..11,y=9..11,z=9..11']) == 38
    assert solve(['on x=10..12,y=10..12,z=10..12','on x=11..13,y=11..13,z=11..13','off x=9..11,y=9..11,z=9..11','on x=10..10,y=10..10,z=10..10']) == 39

    with open('example_input_2.txt', 'r') as f:
        assert solve([x.strip() for x in f.readlines()]) == 2758514936282235

    with open('input.txt', 'r') as f:
        start = time.perf_counter()
        print(solve([x.strip() for x in f.readlines()]))
        print(time.perf_counter() - start)

if __name__ == "__main__":
	main()
