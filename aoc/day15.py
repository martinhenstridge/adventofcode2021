import math
import heapq
from . import util


def get_riskmap(lines):
    riskmap = []
    side = None
    for line in lines:
        if line and not side:
            side = len(line)
        for risk in line:
            riskmap.append(int(risk))
    return riskmap, side


def get_neighbours(side, p):
    neighbours = []

    row, col = divmod(p, side)
    if col > 0:
        neighbours.append(p - 1)
    if col < side - 1:
        neighbours.append(p + 1)
    if row > 0:
        neighbours.append(p - side)
    if row < side - 1:
        neighbours.append(p + side)

    return neighbours


def make_extended_riskmap(riskmap, side, factor):
    extended = [0] * (side * side * factor * factor)
    for p in range(side * side):
        row, col = divmod(p, side)
        for extrow in range(factor):
            for extcol in range(factor):
                er = row + extrow * side
                ec = col + extcol * side
                extp = ec + er * side * factor
                extended[extp] = (riskmap[p] + extrow + extcol - 1) % 9 + 1
    return extended


def manhattan(side, p):
    row, col = divmod(p, side)
    return (side - 1 - row) + (side - 1 - col)


def find_lowest_risk_path(riskmap, side):
    goal = len(riskmap) - 1

    bestmap = [math.inf] * side * side
    bestmap[0] = 0

    pending = []
    heapq.heappush(pending, (0, 0))

    while pending:
        _, p = heapq.heappop(pending)
        if p == goal:
            break

        risksofar = bestmap[p]
        for n in get_neighbours(side, p):
            risk = risksofar + riskmap[n]
            if risk < bestmap[n]:
                bestmap[n] = risk
                priority = risk + manhattan(side, n)
                heapq.heappush(pending, (priority, n))

    return bestmap[goal]


def run():
    inputlines = util.get_input_lines("15.txt")

    riskmap, side = get_riskmap(inputlines)
    risk1 = find_lowest_risk_path(riskmap, side)

    extended = make_extended_riskmap(riskmap, side, 5)
    risk2 = find_lowest_risk_path(extended, 5 * side)

    return risk1, risk2
