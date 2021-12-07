from . import util


def get_positions(lines):
    return [int(p) for line in lines for p in line.split(",") if line]


def triangle(n):
    return (n * (n + 1)) // 2


@util.memoize
def cost_linear(target, positions):
    return sum(abs(p - target) for p in positions)


@util.memoize
def cost_triangle(target, positions):
    return sum(triangle(abs(p - target)) for p in positions)


def find_minimum_cost(positions, cost):
    pmin = min(positions)
    pmax = max(positions)
    cmin = cost(pmin, positions)
    cmax = cost(pmax, positions)

    # Something vaguely resembling interval bisection...
    while True:
        pmid = (pmin + pmax) // 2
        cmid = cost(pmid, positions)

        # The mid-point is hitting the edge of the range, so we must be left
        # with a range of width 1. The minimum is then whichever of the two
        # limiting values has the smaller cost.
        if pmid == pmin or pmid == pmax:
           return min(cmin, cmax)

        if cmax < cmin:
            pmin = pmid
            cmin = cmid
            continue
        if cmin < cmax:
            pmax = pmid
            cmax = cmid
            continue

        # The min and max limiting positions have equal cost. Arbitrarily bump
        # lower limit to get things moving again.
        pmin += 1
        cmin = cost(pmin, positions)


def run():
    inputlines = util.get_input_lines("07.txt")
    positions = get_positions(inputlines)

    cost1 = find_minimum_cost(positions, cost_linear)
    cost2 = find_minimum_cost(positions, cost_triangle)

    return cost1, cost2
