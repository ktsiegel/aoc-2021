from copy import deepcopy

def generate_cube_space(cube_dim):
    cube_space = []
    for i in range(cube_dim):
        rows = []
        for j in range(cube_dim):
            row = [False] * cube_dim
            rows.append(row)
        cube_space.append(rows)
    return cube_space

def cube_dim_to_coord_val(dim):
    return dim - 50

def coord_val_to_cube_dim(val):
    return val + 50

def parse_step(step):
    (setting, coords_str) = step.strip().split(' ')
    assert setting == 'on' or setting == 'off'
    coord_bounds = [[int(x) for x in coords[2:].split('..')] for coords in coords_str.split(',')]
    return setting, coord_bounds

# def is_valid_index(cube, coord):
#     x = coord[0]
#     y = coord[1]
#     z = coord[2]
#     if x < 0 or x >= len(cube):
#         return False
#     if y < 0 or y >= len(cube[0]):
#         return False
#     if z < 0 or z >= len(cube[0][0]):
#         return False
#     return True

def count_on_cubes(cube_space):
    count = 0
    for x in range(len(cube_space)):
        for y in range(len(cube_space[0])):
            for z in range(len(cube_space[0][0])):
                if cube_space[x][y][z]:
                    count += 1
    return count

# bound are inclusive []
# coord bounds can be negative. cube space dims are positive indices
def coord_bounds_to_cube_space_dims(coord_bounds, max_dim):
    [x_min, x_max] = [coord_val_to_cube_dim(x) for x in coord_bounds[0]]
    [y_min, y_max] = [coord_val_to_cube_dim(y) for y in coord_bounds[1]]
    [z_min, z_max] = [coord_val_to_cube_dim(z) for z in coord_bounds[2]]
    x_min = max(0, x_min)
    x_max = min(max_dim, x_max)
    y_min = max(0, y_min)
    y_max = min(max_dim, y_max)
    z_min = max(0, z_min)
    z_max = min(max_dim, z_max)
    return [[x_min, x_max], [y_min, y_max], [z_min, z_max]]

def apply_initialization_step(cube_space, step):
    # updated_cube = deepcopy(cube_space)
    # setting: on or off
    (setting, coord_bounds) = parse_step(step)
    dims = coord_bounds_to_cube_space_dims(coord_bounds, len(cube_space)-1)
    is_on = setting == 'on'
    for x in range(dims[0][0], dims[0][1]+1):
        for y in range(dims[1][0], dims[1][1]+1):
            for z in range(dims[2][0], dims[2][1]+1):
                cube_space[x][y][z] = is_on

def solve(input_lines):
    cube_dim = 101 # -50...50
    cube_space = generate_cube_space(cube_dim)
    for l in input_lines:
        apply_initialization_step(cube_space, l)
    return count_on_cubes(cube_space)

def main():
    with open('example_input.txt', 'r') as f:
        ans = solve([x.strip() for x in f.readlines()])
        assert ans == 590784

    with open('input.txt', 'r') as f:
        ans = solve([x.strip() for x in f.readlines()])
        print(ans)



if __name__ == "__main__":
	main()
