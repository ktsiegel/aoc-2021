from copy import deepcopy

def in_area(point, x_params, y_params):
    return point[0] >= x_params[0] and point[0] <= x_params[1] \
        and point[1] >= y_params[0] and point[1] <= y_params[1]

def valid_initial_velocity(v, x_params, y_params):
    pos = (0,0)
    velocity = v
    max_y = 0
    while pos[0] <= x_params[1] and pos[1] >= y_params[0]:
        pos = (pos[0] + velocity[0], pos[1] + velocity[1])
        max_y = max(pos[1], max_y)

        if in_area(pos, x_params, y_params):
            return True, max_y

        new_v_x = velocity[0]
        if new_v_x > 0:
            new_v_x -= 1
        elif new_v_x < 0:
            new_v_x += 1
        velocity = (new_v_x, velocity[1] - 1)
    return False, max_y

def find_highest_initial_velocity(x_params, y_params):
    global_max_y = -1000
    total_valid = 0
    valid = []
    for x in range(0, x_params[1]+1):
        for y in range(y_params[0], 1000):
            (is_valid, max_y) = valid_initial_velocity((x,y), x_params, y_params)
            if is_valid:
                global_max_y = max(global_max_y, max_y)
                total_valid += 1
                valid.append([x, y])

    return global_max_y, total_valid

def main():
    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]

    [x_params, y_params] = lines[0][13:].split(', ')
    [x, x_param_values] = x_params.split('=')
    [y, y_param_values] = y_params.split('=')
    [x_start, x_end] = [int(x) for x in x_param_values.split('..')]
    [y_start, y_end] = [int(x) for x in y_param_values.split('..')]
    print('x: {} to {}, y: {} to {}'.format(x_start, x_end, y_start, y_end))

    x_range = (x_start, x_end)
    y_range = (y_start, y_end)

    # for example input only
    # assert valid_initial_velocity((7, 2), x_range, y_range) == (True, 3)
    # assert valid_initial_velocity((6, 3), x_range, y_range) == (True, 6)
    # assert valid_initial_velocity((6, 0), x_range, y_range) == (True, 0)
    print(find_highest_initial_velocity(x_range, y_range))


if __name__ == "__main__":
	main()
