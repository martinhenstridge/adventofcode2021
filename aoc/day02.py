from . import util


def get_instructions(lines):
    instructions = []
    for line in lines:
        if not line:
            continue
        parts = line.split(" ")
        instructions.append((parts[0], int(parts[1])))
    return instructions


def run_part1(instructions):
    horiz = 0
    depth = 0

    for direction, units in instructions:
        if direction == "forward":
            horiz += units
        elif direction == "up":
            depth -= units
        elif direction == "down":
            depth += units
        else:
            assert False

    return horiz, depth


def run_part2(instructions):
    horiz = 0
    depth = 0
    aim = 0

    for direction, units in instructions:
        if direction == "forward":
            horiz += units
            depth += aim * units
        elif direction == "up":
            aim -= units
        elif direction == "down":
            aim += units
        else:
            assert False

    return horiz, depth


def run():
    inputlines = util.get_input_lines("02.txt")
    instructions = get_instructions(inputlines)

    horiz1, depth1 = run_part1(instructions)
    horiz2, depth2 = run_part2(instructions)

    return horiz1 * depth1, horiz2 * depth2
