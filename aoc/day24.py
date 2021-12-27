from . import util


def get_constants(lines):
    consts = []

    chunklen = len(lines) // 14
    for i in range(14):
        start = i * chunklen
        a = int(lines[start + 4].split()[-1])
        b = int(lines[start + 5].split()[-1])
        c = int(lines[start + 15].split()[-1])
        consts.append((a, b, c))

    return consts


def derive_constraints(constants):
    constraints = []

    stack = []
    for i, (a, b, c) in enumerate(constants):
        if a == 1:
            stack.append((i, c))
        elif a == 26:
            _i, _c = stack.pop()
            constraints.append((i, _i, _c + b))

    return constraints


def solve(goal, constraints):
    digits = [goal] * 14
    for i, j, delta in constraints:
        digits[i] = digits[j] + delta

    return int("".join(str(digit) for digit in digits))


def run():
    inputlines = util.get_input_lines("24.txt")
    constants = get_constants(inputlines)
    constraints = derive_constraints(constants)

    # Credit for this goes to:
    # https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs
    hi = solve(9, [(i, j, d) if d < 0 else (j, i, -d) for i, j, d in constraints])
    lo = solve(1, [(i, j, d) if d > 0 else (j, i, -d) for i, j, d in constraints])

    return hi, lo
