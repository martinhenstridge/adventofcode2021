from . import util


def get_depths(lines):
    return [int(line) for line in lines if line]


def count_increases1(depths):
    count = 0
    prev = depths[0]
    for curr in depths[1:]:
        if curr > prev:
            count += 1
        prev = curr
    return count


def count_increases3(depths):
    count = 0
    prev = depths[:3]
    for curr in depths[3:]:
        if curr > prev[0]:
            count += 1
        prev = [prev[1], prev[2], curr]
    return count


def run():
    inputlines = util.get_input_lines("01.txt")
    depths = get_depths(inputlines)

    increases1 = count_increases1(depths)
    increases3 = count_increases3(depths)

    return increases1, increases3
