from . import util


#    0:      1:      2:      3:      4:
#   aaaa    ....    aaaa    aaaa    ....
#  b    c  .    c  .    c  .    c  b    c
#  b    c  .    c  .    c  .    c  b    c
#   ....    ....    dddd    dddd    dddd
#  e    f  .    f  e    .  .    f  .    f
#  e    f  .    f  e    .  .    f  .    f
#   gggg    ....    gggg    gggg    ....
#
#    5:      6:      7:      8:      9:
#   aaaa    aaaa    aaaa    aaaa    aaaa
#  b    .  b    .  .    c  b    c  b    c
#  b    .  b    .  .    c  b    c  b    c
#   dddd    dddd    ....    dddd    dddd
#  .    f  e    f  .    f  e    f  .    f
#  .    f  e    f  .    f  e    f  .    f
#   gggg    gggg    ....    gggg    gggg


def get_entries(lines):
    entries = []
    for line in lines:
        if line:
            l, r = line.split(" | ")
            entries.append((
                [frozenset(n) for n in l.split()],
                [frozenset(n) for n in r.split()]))
    return entries


def count_uniques(entries):
    count = 0
    for _, output in entries:
        for digit in output:
            if len(digit) in {2, 3, 4, 7}:
                count += 1
    return count


def find_mapping(patterns):
    known = {}

    # First, map the numbers which use a unique number of segments.
    for pattern in patterns:
        length = len(pattern)
        if length == 2:
            known["1"] = pattern
        elif length == 3:
            known["7"] = pattern
        elif length == 4:
            known["4"] = pattern
        elif length == 7:
            known["8"] = pattern

    # Of the numbers which use 6 segments:
    # - only '9' is a strict superset of '4'
    # - only '6' isn't a strict superset of '1'
    # - '0' must be the one left over
    for pattern in patterns:
        if len(pattern) == 6:
            if pattern > known["4"]:
                known["9"] = pattern
            elif not pattern > known["1"]:
                known["6"] = pattern
            else:
                known["0"] = pattern

    # Of the numbers which use 5 segments:
    # - only '3' is a strict superset of '1'
    # - only '5' is a strict subset of '6'
    # - '2' must be the one left over
    for pattern in patterns:
        if len(pattern) == 5:
            if pattern > known["1"]:
                known["3"] = pattern
            elif pattern < known["6"]:
                known["5"] = pattern
            else:
                known["2"] = pattern

    # Return the inverse (i.e. pattern:number) mapping.
    return {v: k for k, v in known.items()}


def decode_output(mapping, encoded):
    return int("".join(mapping[digit] for digit in encoded))


def run():
    inputlines = util.get_input_lines("08.txt")
    entries = get_entries(inputlines)

    count = count_uniques(entries)
    total = 0
    for patterns, output in entries:
        mapping = find_mapping(patterns)
        total += decode_output(mapping, output)

    return count, total
