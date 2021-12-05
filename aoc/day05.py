import re
from collections import defaultdict
from . import util


def parse_vent_line(line):
    m = re.fullmatch(r"(\d+),(\d+) -> (\d+),(\d+)", line)
    return (int(m[1]), int(m[2])), (int(m[3]), int(m[4]))


def get_vent_lines(lines):
    return [parse_vent_line(line) for line in lines if line]


def get_vents_aligned(line):
    (ax, ay), (bx, by) = line

    if ax == bx:
        step = +1 if ay < by else -1
        for y in range(ay, by+step, step):
            yield (ax, y)

    if ay == by:
        step = +1 if ax < bx else -1
        for x in range(ax, bx+step, step):
            yield (x, ay)


def get_vents_diagonal(line):
    (ax, ay), (bx, by) = line
    if (ax == bx) or (ay == by):
        return []

    xstep = +1 if ax < bx else -1
    ystep = +1 if ay < by else -1
    x = ax
    y = ay
    while x != bx+xstep:
        yield (x, y)
        x += xstep
        y += ystep


def run():
    inputlines = util.get_input_lines("05.txt")
    vent_lines = get_vent_lines(inputlines)

    counts = defaultdict(int)

    for vent_line in vent_lines:
        for vent in get_vents_aligned(vent_line):
            counts[vent] += 1
    overlapping1 = sum(1 for c in counts.values() if c > 1)

    for vent_line in vent_lines:
        for vent in get_vents_diagonal(vent_line):
            counts[vent] += 1
    overlapping2 = sum(1 for c in counts.values() if c > 1)

    return overlapping1, overlapping2
