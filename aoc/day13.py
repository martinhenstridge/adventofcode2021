import re
from . import util


def get_dots_folds(lines):
    dots = set()
    folds = []
    lineiter = iter(lines)

    while line := next(lineiter):
        x, y = line.split(",")
        dots.add((int(x), int(y)))

    while line := next(lineiter):
        m = re.fullmatch(r"fold along (x|y)=(\d+)", line)
        axis = m[1]
        coord = int(m[2])
        if axis == "x":
            folds.append((foldx, coord))
        if axis == "y":
            folds.append((foldy, coord))

    return dots, folds


def foldx(axis, dots):
    result = set()
    for x, y in dots:
        if x < axis:
            result.add((x, y))
        else:
            result.add((2*axis - x, y))
    return result


def foldy(axis, dots):
    result = set()
    for x, y in dots:
        if y < axis:
            result.add((x, y))
        else:
            result.add((x, 2*axis - y))
    return result


def run():
    inputlines = util.get_input_lines("13.txt")
    dots, folds = get_dots_folds(inputlines)

    for fold, coord in folds[:1]:
        dots = fold(coord, dots)
    dots1 = dots

    for fold, coord in folds[1:]:
        dots = fold(coord, dots)

    #xmax = max(dots, key=lambda d: d[0])[0]
    #ymax = max(dots, key=lambda d: d[1])[1]

    #for y in range(ymax + 1):
    #    for x in range(xmax + 1):
    #        if (x, y) in dots:
    #            print(" #", end="")
    #        else:
    #            print(" .", end="")
    #    print()

    return len(dots1), "FAGURZHE"
