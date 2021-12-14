import re
import math
from collections import defaultdict
from . import util


def get_first_polymer_rules(lines):
    lineiter = iter(lines)

    first = None
    polymer = defaultdict(int)
    while line := next(lineiter):
        first = line[0]
        for i in range(len(line) - 1):
            polymer[line[i : i+2]] += 1

    # Map each starting pair to the pairs resulting from the insertion.
    rules = {}
    while line := next(lineiter):
        m = re.fullmatch(r"([A-Z]{2}) -> ([A-Z]{1})", line)
        rules[m[1]] = [f"{m[1][0]}{m[2]}", f"{m[2]}{m[1][1]}"]

    return first, polymer, rules


def polymerize(polymer, rules):
    result = defaultdict(int)
    for pair, count in polymer.items():
        for insert in rules[pair]:
            result[insert] += count
    return result


def score(polymer, first):
    counts = defaultdict(int)

    # Count the first element separately, then count the second element in every
    # pair to avoid double counting.
    counts[first] += 1
    for pair, count in polymer.items():
        counts[pair[1]] += count

    # Find the min and max counts then return the difference.
    mincount = math.inf
    maxcount = 0
    for count in counts.values():
        if count < mincount:
            mincount = count
        if count > maxcount:
            maxcount = count
    return maxcount - mincount


def run():
    inputlines = util.get_input_lines("14.txt")
    first, polymer, rules = get_first_polymer_rules(inputlines)

    for _ in range(10):
        polymer = polymerize(polymer, rules)
    score10 = score(polymer, first)

    for _ in range(30):
        polymer = polymerize(polymer, rules)
    score40 = score(polymer, first)

    return score10, score40
