from collections import defaultdict
from . import util


def get_connections(lines):
    connections = defaultdict(list)
    for line in lines:
        if not line:
            continue
        l, r = line.split("-")
        if l != "end" and r != "start":
            connections[l].append(r)
        if r != "end" and l != "start":
            connections[r].append(l)
    return connections


def is_small(cave):
    return cave.lower() == cave


def count_routes1(connections):
    routes = 0

    partials = [["start"]]
    while partials:
        partial = partials.pop()
        for cave in connections[partial[-1]]:
            if cave == "end":
                routes += 1
                continue

            if is_small(cave) and cave in partial:
                continue

            extended = partial[:]
            extended.append(cave)
            partials.append(extended)

    return routes


def count_routes2(connections):
    routes = 0

    partials = [(["start"], False)]
    while partials:
        partial, revisited = partials.pop()
        for cave in connections[partial[-1]]:
            if cave == "end":
                routes += 1
                continue

            revisiting = revisited
            if is_small(cave) and cave in partial:
                if revisited:
                    continue
                revisiting = True

            extended = partial[:]
            extended.append(cave)
            partials.append((extended, revisiting))

    return routes


def run():
    inputlines = util.get_input_lines("12.txt")
    connections = get_connections(inputlines)

    count1 = count_routes1(connections)
    count2 = count_routes2(connections)

    return count1, count2
