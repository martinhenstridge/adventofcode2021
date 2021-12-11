from . import util


def get_octopuses(lines):
    octopuses = []
    for line in lines:
        for char in line:
            octopuses.append(int(char))
    return octopuses


@util.memoize
def get_neighbours(octopus):
    neighbours = []

    orow, ocol = divmod(octopus, 10)
    for nrow in range(orow - 1, orow + 2):
        if 0 <= nrow < 10:
            for ncol in range(ocol - 1, ocol + 2):
                if 0 <= ncol < 10:
                    neighbour = ncol + 10 * nrow
                    if neighbour != octopus:
                        neighbours.append(ncol + 10 * nrow)

    return neighbours


def evolve(octopuses):
    flashes = 0
    pending = set()

    # First increase the energy of every octopus by 1.
    for o in range(100):
        octopuses[o] += 1
        if octopuses[o] == 10:
            octopuses[o] = 0
            flashes += 1
            pending.add(o)

    # Now recursively propagate flashes to neighbouring octopuses.
    while pending:
        o = pending.pop()
        for n in get_neighbours(o):
            if octopuses[n] == 0:
                continue  # Already flashed
            octopuses[n] += 1
            if octopuses[n] == 10:
                octopuses[n] = 0
                flashes += 1
                pending.add(n)

    return flashes


def run():
    inputlines = util.get_input_lines("11.txt")
    octopuses = get_octopuses(inputlines)

    flashes = sum(evolve(octopuses) for _ in range(100))

    steps = 101
    while evolve(octopuses) != 100:
        steps += 1

    return flashes, steps
