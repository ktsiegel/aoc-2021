from copy import deepcopy
from math import floor, ceil

def add_to_leftmost(number, val_to_add):
    if type(number) == int:
        return number + val_to_add
    return [add_to_leftmost(number[0], val_to_add), number[1]]

def add_to_rightmost(number, val_to_add):
    if type(number) == int:
        return number + val_to_add
    return [number[0], add_to_rightmost(number[1], val_to_add)]

# checks if a snailfish number needs to be exploded and if so, explodes it once
# returns had_explosion, new_value
def explode_snailfish_number(number):
    (had_explosion, updated_number, _, _) = explode_snailfish_number_helper(number, 0)
    return (had_explosion, updated_number)

def explode_snailfish_number_helper(number, depth):
    if type(number) == int:
        return False, number, None, None
    if depth < 4:
        (had_explosion, result, left_num, right_num) = explode_snailfish_number_helper(number[0], depth + 1)
        if had_explosion:
            updated_right = number[1]
            if had_explosion and right_num is not None:
                updated_right = add_to_leftmost(updated_right, right_num)
            return had_explosion, [result, updated_right], left_num, None
        (had_explosion, result, left_num, right_num) = explode_snailfish_number_helper(number[1], depth + 1)
        updated_left = number[0]
        if had_explosion and left_num is not None:
            updated_left = add_to_rightmost(updated_left, left_num)
        return had_explosion, [updated_left, result], None, right_num
    # pair is comprised of two regular numbers [X, Y]
    return True, 0, number[0], number[1]


# checks if a snailfish number needs to be split and if so, splits it once
def split_snailfish_number(number):
    if type(number) == int:
        if number >= 10:
            # needs split
            return True, [floor(number/2), ceil(number/2)]
        return False, number
    (left_had_split, updated_left) = split_snailfish_number(number[0])
    if left_had_split:
        return left_had_split, [updated_left, number[1]]
    (right_had_split, updated_right) = split_snailfish_number(number[1])
    return right_had_split, [number[0], updated_right]

# reduces the snailfish number 'number'
def reduce_snailfish_number(number):
    curr = number
    while True:
        # if any pair is nested inside four pairs, the leftmost such pair explodes
        (had_explosion, curr) = explode_snailfish_number(curr)

        # if any regular number is 10 or greater, the leftmost such regular number
        # splits
        if had_explosion:
            continue
        (had_split, curr) = split_snailfish_number(curr)
        if not had_split:
            break
    return curr

# adds the pair 'left' with the pair 'right' and then reduces
def add_snailfish_numbers(left, right):
    return reduce_snailfish_number([left, right])

# parses a snailfish number represented by a string into nested pairs
def parse_snailfish_number(number):
    if number[0] != '[':
        return int(number)

    depth = 0
    first_elem = ''
    second_elem = ''
    for i in range(len(number)):
        if number[i] == '[':
            depth += 1
        elif number[i] == ']':
            depth -= 1
        elif number[i] == ',' and depth == 1:
            first_elem = number[1:i]
            second_elem = number[i+1:-1]
            break
    return [parse_snailfish_number(first_elem), parse_snailfish_number(second_elem)]

def sum_snailfish_list(str_input):
    lines = str_input.split('\n')
    assert len(lines) > 0
    value = parse_snailfish_number(lines[0])
    for i in range(1, len(lines)):
        value = add_snailfish_numbers(value, parse_snailfish_number(lines[i]))
    return value

def compute_magnitude(number):
    if type(number) == int:
        return number
    return compute_magnitude(number[0]) * 3 + compute_magnitude(number[1]) * 2

# raw input, with each line separated by \n
def do_snailfish_hw(input_lines):
    summed_value = sum_snailfish_list(input_lines)
    return compute_magnitude(summed_value)

def find_largest_magnitude_of_any_pair(input_lines):
    lines = input_lines.split('\n')
    max_mag = 0
    for i in range(0, len(lines)):
        for j in range(0, len(lines)):
            if i == j:
                continue
            mag = compute_magnitude(add_snailfish_numbers(parse_snailfish_number(lines[i]), parse_snailfish_number(lines[j])))
            max_mag = max(max_mag, mag)
    return max_mag

def test_parse_snailfish_number():
    assert parse_snailfish_number('[1,2]') == [1,2]
    assert parse_snailfish_number('[[1,2],3]') == [[1,2],3]
    assert parse_snailfish_number('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]') == [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
    assert parse_snailfish_number('[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]') == [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]

def test_add_to_leftmost():
    assert add_to_leftmost([[1,2],3], 4) == [[5,2],3]
    assert add_to_leftmost([[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]], 2) == [[[11,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]

def test_add_to_rightmost():
    assert add_to_rightmost([[1,2],3], 4) == [[1,2],7]
    assert add_to_rightmost([[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]], 2) == [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],5]]

def test_explode_snailfish_number():
    assert explode_snailfish_number([[[[[9,8],1],2],3],4]) == (True, [[[[0,9],2],3],4])
    assert explode_snailfish_number([7,[6,[5,[4,[3,2]]]]]) == (True, [7,[6,[5,[7,0]]]])
    assert explode_snailfish_number([[6,[5,[4,[3,2]]]],1]) == (True, [[6,[5,[7,0]]],3])
    assert explode_snailfish_number([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == (True, [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
    assert explode_snailfish_number([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == (True, [[3,[2,[8,0]]],[9,[5,[7,0]]]])

def test_split_snailfish_number():
    assert split_snailfish_number([[[[0,7],4],[15,[0,13]]],[1,1]]) == (True, [[[[0,7],4],[[7,8],[0,13]]],[1,1]])
    assert split_snailfish_number([[[[0,7],4],[[7,8],[0,13]]],[1,1]]) == (True, [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]])
    assert split_snailfish_number([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]) == (False, [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]])

def test_add_snailfish_numbers():
    assert add_snailfish_numbers([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]], [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]) == [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
    assert add_snailfish_numbers([[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]], [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]) == [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
    assert add_snailfish_numbers([[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]], [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]) == [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]

def test_sum_snailfish_list():
    assert sum_snailfish_list('''[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]''') == [[[[5,0],[7,4]],[5,5]],[6,6]]
    assert sum_snailfish_list('''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]''') == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
    assert sum_snailfish_list('''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]''') == [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]

def test_compute_magnitude():
    assert compute_magnitude([[9,1],[1,9]]) == 129
    assert compute_magnitude([[1,2],[[3,4],5]]) == 143
    assert compute_magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == 1384
    assert compute_magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488

def main():
    test_parse_snailfish_number()
    test_add_to_leftmost()
    test_add_to_rightmost()
    test_explode_snailfish_number()
    test_split_snailfish_number()
    test_add_snailfish_numbers()
    test_sum_snailfish_list()
    test_compute_magnitude()

    # part 1
    with open('example_input.txt', 'r') as f:
        example_lines = '\n'.join([x.strip() for x in f.readlines()])
    assert do_snailfish_hw(example_lines) == 4140

    with open('input.txt', 'r') as f:
        lines = '\n'.join([x.strip() for x in f.readlines()])
    print(do_snailfish_hw(lines))

    # part 2
    assert find_largest_magnitude_of_any_pair(example_lines) == 3993
    print(find_largest_magnitude_of_any_pair(lines))

if __name__ == "__main__":
	main()
