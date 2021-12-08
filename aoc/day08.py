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

LENGTHS = {
    "0": len("abcefg"),
    "1": len("cf"),
    "2": len("acdeg"),
    "3": len("acdfg"),
    "4": len("bcdf"),
    "5": len("abdfg"),
    "6": len("abdefg"),
    "7": len("acf"),
    "8": len("abcdefg"),
    "9": len("abcdfg"),
}


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
    uniqs = {
        LENGTHS["1"],
        LENGTHS["4"],
        LENGTHS["7"],
        LENGTHS["8"],
    }
    for _, output in entries:
        for digit in output:
            if len(digit) in uniqs:
                count += 1
    return count


def find_with_length(length, patterns):
    for p in patterns:
        if len(p) == length:
            return p


def find_mapping(patterns):
    known = {}

    # First, map the numbers which use a unique number of segments.
    for n in ["1", "4", "7", "8"]:
        known[n] = find_with_length(LENGTHS[n], patterns)

    # Of the numbers which use 6 segments:
    # - only '9' is a strict superset of '4'
    # - only '6' isn't a strict superset of '1'
    # - '0' must be the one left over
    unknown = {p for p in patterns if len(p) == 6}
    for pattern in unknown:
        if pattern > known["4"]:
            known["9"] = pattern
            unknown.discard(pattern)
            break
    for pattern in unknown:
        if not pattern > known["1"]:
            known["6"] = pattern
            unknown.discard(pattern)
            break
    known["0"] = unknown.pop()

    # Of the numbers which use 5 segments:
    # - only '3' is a strict superset of '1'
    # - only '5' is a strict subset of '6'
    # - '2' must be the one left over
    unknown = {p for p in patterns if len(p) == 5}
    for pattern in unknown:
        if pattern > known["1"]:
            known["3"] = pattern
            unknown.discard(pattern)
            break
    for pattern in unknown:
        if pattern < known["6"]:
            known["5"] = pattern
            unknown.discard(pattern)
            break
    known["2"] = unknown.pop()

    # Return the inverse (i.e. segments:number) mapping.
    return {v: k for k, v in known.items()}


def decode_output(mapping, encoded):
    return "".join(mapping[digit] for digit in encoded)


def run():
    inputlines = util.get_input_lines("08.txt")
    entries = get_entries(inputlines)

    count = count_uniques(entries)
    total = 0
    for i, (patterns, output) in enumerate(entries):
        mapping = find_mapping(patterns)
        decoded = decode_output(mapping, output)
        total += int(decoded)

    return count, total
