import re
from collections import defaultdict
from . import util


TRANSFORMS = [
    # rotation around +ve z-axis
    lambda p: (+p[0], +p[1], +p[2]),
    lambda p: (+p[1], -p[0], +p[2]),
    lambda p: (-p[0], -p[1], +p[2]),
    lambda p: (-p[1], +p[0], +p[2]),

    # rotation around -ve z-axis
    lambda p: (-p[1], -p[0], -p[2]),
    lambda p: (-p[0], +p[1], -p[2]),
    lambda p: (+p[1], +p[0], -p[2]),
    lambda p: (+p[0], -p[1], -p[2]),

    # rotation around +ve y-axis
    lambda p: (+p[0], -p[2], +p[1]),
    lambda p: (-p[2], -p[0], +p[1]),
    lambda p: (-p[0], +p[2], +p[1]),
    lambda p: (+p[2], +p[0], +p[1]),

    # rotation around -ve y-axis
    lambda p: (-p[2], +p[0], -p[1]),
    lambda p: (+p[0], +p[2], -p[1]),
    lambda p: (+p[2], -p[0], -p[1]),
    lambda p: (-p[0], -p[2], -p[1]),

    # rotation around +ve x-axis
    lambda p: (-p[1], -p[2], +p[0]),
    lambda p: (-p[2], +p[1], +p[0]),
    lambda p: (+p[1], +p[2], +p[0]),
    lambda p: (+p[2], -p[1], +p[0]),

    # rotation around -ve x-axis
    lambda p: (-p[2], -p[1], -p[0]),
    lambda p: (-p[1], +p[2], -p[0]),
    lambda p: (+p[2], +p[1], -p[0]),
    lambda p: (+p[1], -p[2], -p[0]),
]


def get_beacon_positions(lines):
    scanner = None
    beacons = []
    for line in lines:
        if not line:
            yield scanner, beacons
        elif m := re.fullmatch(r"--- scanner (\d+) ---", line):
            scanner = int(m[1])
            beacons = []
        else:
            p = line.split(",")
            beacon = int(p[0]), int(p[1]), int(p[2])
            beacons.append(beacon)


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def offset_position(reference, position):
    return (
        reference[0] - position[0],
        reference[1] - position[1],
        reference[2] - position[2],
    )


def check_for_overlap(references, beacons):
    offsets = defaultdict(int)
    for reference in references:
        for beacon in beacons:
            offset = offset_position(beacon, reference)
            offsets[offset] += 1
            if offsets[offset] == 12:
                return True, offset
    return False, None


def find_overlapping(knowns, unknowns):
    for known in knowns:
        for scanner, beacons in unknowns.items():
            for transform in TRANSFORMS:
                transformed = [transform(beacon) for beacon in beacons]
                overlapping, offset = check_for_overlap(known, transformed)
                if overlapping:
                    return scanner, offset, [
                        offset_position(beacon, offset)
                        for beacon in transformed
                    ]


def run():
    inputlines = util.get_input_lines("19.txt")
    unknowns = {
        scanner: beacons
        for scanner, beacons
        in get_beacon_positions(inputlines)
    }

    knowns = [unknowns.pop(0)]
    scanners = {0: (0, 0, 0)}

    while unknowns:
        scanner, offset, corrected = find_overlapping(knowns, unknowns)
        knowns.insert(0, corrected)
        scanners[scanner] = offset
        del unknowns[scanner]

    beacons = set()
    for known in knowns:
        for beacon in known:
            beacons.add(beacon)
    count = len(beacons)

    max_distance = 0
    while scanners:
        _, this_position = scanners.popitem()
        for that_position in scanners.values():
            distance = manhattan_distance(this_position, that_position)
            if distance > max_distance:
                max_distance = distance

    return count, max_distance
