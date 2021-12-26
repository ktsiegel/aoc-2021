from copy import deepcopy
from math import trunc, log10

ALU_MAPPINGS = {'w': 0, 'x': 1, 'y': 2, 'z': 3}

# returns the value if it's an int, otherwise gets the value from the alu
def get_instruction_val(alu, instruction):
    if len(instruction) < 3:
        return None
    val = instruction[2]
    if val.lstrip('-').isdigit():
        return int(val)
    return alu[ALU_MAPPINGS[val]]

# def process_instructions(instructions, digits):
#     alu = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
#     i = 0
#     for instruction in instructions:
#         if instruction[0] == 'inp':
#             alu[instruction[1]] = digits[i]
#             i += 1
#         else:
#             v = get_instruction_val(alu, instruction[2]) # value for b
#             a_reg = instruction[1] # register for a
#             ins = instruction[0]
#             if ins == 'add':
#                 alu[a_reg] += v
#             elif ins == 'mul':
#                 alu[a_reg] *= v
#             elif ins == 'div':
#                 assert v != 0
#                 alu[a_reg] = trunc(alu[a_reg] / v)
#             elif ins == 'mod':
#                 assert v != 0
#                 alu[a_reg] %= v
#             elif ins == 'eql':
#                 if alu[a_reg] == v:
#                     alu[a_reg] = 1
#                 else:
#                     alu[a_reg] = 0
#     return alu['z']

def update_alu(alu, reg, val):
    alu[ALU_MAPPINGS[reg]] = val

def process_instructions(instructions):
    alus = {(0,0,0,0): 0}
    j = 0
    for instruction in instructions:
        j += 1
        new_alus = dict()
        for tuple_alu, num in alus.items():
            alu = list(tuple_alu)
            if instruction[0] == 'inp':
                for i in range(1, 10):
                    alu_with_inp = deepcopy(alu)
                    update_alu(alu_with_inp, instruction[1], i)
                    new_alu = tuple(alu_with_inp)
                    new_digit_series = num * 10 + i
                    if new_alu in new_alus.keys():
                        new_alus[new_alu] = max(new_digit_series, new_alus[new_alu])
                    else:
                        new_alus[new_alu] = new_digit_series
            else:
                a_reg = ALU_MAPPINGS[instruction[1]] # index of register for a
                v = get_instruction_val(alu, instruction) # value for b
                ins = instruction[0]
                if ins == 'add':
                    alu[a_reg] += v
                elif ins == 'mul':
                    alu[a_reg] *= v
                elif ins == 'div':
                    assert v != 0
                    alu[a_reg] = trunc(alu[a_reg] / v)
                elif ins == 'mod':
                    assert v != 0
                    alu[a_reg] %= v
                elif ins == 'eql':
                    if alu[a_reg] == v:
                        alu[a_reg] = 1
                    else:
                        alu[a_reg] = 0
        alus = new_alus
        print(j)
    max_digits = 0
    min_digits = None
    for alu, digits in alus.items():
        if alu[ALU_MAPPINGS['z']] == 0:
            max_digits = max(max_digits, digits)
            if min_digits is None:
                min_digits = digits
            else:
                min_digits = min(min_digits, digits)
            print(alu, digits)
    return max_digits, min_digits

def solve(input_lines):
    instructions = [line.strip().split(' ') for line in input_lines]
    print(process_instructions(instructions))

def main():
    example_binary = '''inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2'''.split('\n')
    # print(process_instructions(example_binary, [13]))

    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]


    print(solve(lines))


if __name__ == "__main__":
	main()
