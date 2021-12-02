from . import util


def get_depths(lines):
    return [int(line) for line in lines if line]


def count_increases(depths, window):
    count = 0
    for idx in range(len(depths) - window):
        if depths[idx + window] > depths[idx]:
            count += 1
    return count


def run():
    inputlines = util.get_input_lines("01.txt")
    depths = get_depths(inputlines)

    increases1 = count_increases(depths, 1)
    increases3 = count_increases(depths, 3)

    return increases1, increases3
