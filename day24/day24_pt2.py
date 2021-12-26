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
                        new_alus[new_alu] = min(new_digit_series, new_alus[new_alu])
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
                new_alu = tuple(alu)
                if new_alu[ALU_MAPPINGS['z']] < 1000000:
                    if new_alu not in new_alus.keys() or num < new_alus[new_alu]:
                        new_alus[new_alu] = num
        alus = new_alus
        print('instruction', j)
    min_digits = None
    for alu, digits in alus.items():
        if alu[ALU_MAPPINGS['z']] == 0:
            if min_digits is None:
                min_digits = digits
            else:
                min_digits = min(min_digits, digits)
            print(alu, digits)
    return min_digits

def solve(input_lines):
    instructions = [line.strip().split(' ') for line in input_lines]
    print(process_instructions(instructions))

def main():
    with open('input.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    solve(lines)

if __name__ == "__main__":
	main()
