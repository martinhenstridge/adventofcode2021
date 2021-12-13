import re
from . import util


LETTERS_TO_DOTS = {
    "A": [
              (1,0),(2,0),
        (0,1),            (3,1),
        (0,2),            (3,2),
        (0,3),(1,3),(2,3),(3,3),
        (0,4),            (3,4),
        (0,5),            (3,5),
    ],
    "E": [
        (0,0),(1,0),(2,0),(3,0),
        (0,1),
        (0,2),(1,2),(2,2),
        (0,3),
        (0,4),
        (0,5),(1,5),(2,5),(3,5),
    ],
    "F": [
        (0,0),(1,0),(2,0),(3,0),
        (0,1),
        (0,2),(1,2),(2,2),
        (0,3),
        (0,4),
        (0,5),
    ],
    "G": [
              (1,0),(2,0),
        (0,1),            (3,1),
        (0,2),
        (0,3),      (2,3),(3,3),
        (0,4),            (3,4),
              (1,5),(2,5),(3,5),
    ],
    "H": [
        (0,0),            (3,0),
        (0,1),            (3,1),
        (0,2),(1,2),(2,2),(3,2),
        (0,3),            (3,3),
        (0,4),            (3,4),
        (0,5),            (3,5),
    ],
    "R": [
        (0,0),(1,0),(2,0),
        (0,1),            (3,1),
        (0,2),            (3,2),
        (0,3),(1,3),(2,3),
        (0,4),      (2,4),
        (0,5),            (3,5),
    ],
    "U": [
        (0,0),            (3,0),
        (0,1),            (3,1),
        (0,2),            (3,2),
        (0,3),            (3,3),
        (0,4),            (3,4),
              (1,5),(2,5),
    ],
    "Z": [
        (0,0),(1,0),(2,0),(3,0),
                          (3,1),
                    (2,2),
              (1,3),
        (0,4),
        (0,5),(1,5),(2,5),(3,5),
    ],
}

DOTS_TO_LETTERS = {frozenset(v): k for k, v in LETTERS_TO_DOTS.items()}



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


def parse_code(dots):
    letters = [set() for _ in range(8)]
    for x, y in dots:
        div, mod = divmod(x, 5)
        letters[div].add((mod, y))
    return "".join(DOTS_TO_LETTERS[frozenset(letter)] for letter in letters)


def run():
    inputlines = util.get_input_lines("13.txt")
    dots, folds = get_dots_folds(inputlines)

    for fold, coord in folds[:1]:
        dots = fold(coord, dots)
    dots1 = dots

    for fold, coord in folds[1:]:
        dots = fold(coord, dots)
    dots2 = dots

    return len(dots1), parse_code(dots2)
