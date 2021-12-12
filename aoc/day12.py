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


def find_routes1(connections):
    routes = []

    partials = [["start"]]
    while partials:
        partial = partials.pop()
        for cave in connections[partial[-1]]:
            if is_small(cave) and cave in partial:
                continue
            extended = partial[:]
            extended.append(cave)
            if cave == "end":
                routes.append(extended)
            else:
                partials.append(extended)

    return routes


def find_routes2(connections):
    routes = []

    partials = [(["start"], False)]
    while partials:
        partial, revisited = partials.pop()
        for cave in connections[partial[-1]]:
            revisiting = revisited
            if is_small(cave) and cave in partial:
                if revisited:
                    continue
                revisiting = True
            extended = partial[:]
            extended.append(cave)
            if cave == "end":
                routes.append(extended)
            else:
                partials.append((extended, revisiting))

    return routes


def run():
    inputlines = util.get_input_lines("12.txt")
    connections = get_connections(inputlines)

    routes1 = find_routes1(connections)
    routes2 = find_routes2(connections)

    return len(routes1), len(routes2)
