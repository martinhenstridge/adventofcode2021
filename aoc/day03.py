from . import util


def get_numstrs(lines):
    return [line for line in lines if line]


def calculate_gamma_epsilon(numstrs):
    half = len(numstrs) // 2
    length = len(numstrs[0])
    freqs0 = [0] * length

    for numstr in numstrs:
        for i, digit in enumerate(numstr):
            if digit == "0":
                freqs0[i] += 1

    gdigits = ["0" if freqs0[i] > half else "1" for i in range(length)]
    edigits = ["1" if freqs0[i] > half else "0" for i in range(length)]

    return int("".join(gdigits), 2), int("".join(edigits), 2)


def most_common_digit(numstrs, position):
    count0 = 0
    count1 = 0

    for numstr in numstrs:
        if numstr[position] == "0":
            count0 += 1
        else:
            count1 += 1

    # For both "oxygen generator rating" and "CO2 scrubber rating", 1 is
    # considered more common than 0 in the event of a tie.
    return "0" if count0 > count1 else "1"


def calculate_ogr(candidates):
    position = 0
    while len(candidates) > 1:
        mcd = most_common_digit(candidates, position)
        candidates = [c for c in candidates if c[position] == mcd]
        position += 1
    return int(candidates.pop(), 2)


def calculate_csr(candidates):
    position = 0
    while len(candidates) > 1:
        mcd = most_common_digit(candidates, position)
        candidates = [c for c in candidates if c[position] != mcd]
        position += 1
    return int(candidates.pop(), 2)


def run():
    inputlines = util.get_input_lines("03.txt")
    numstrs = get_numstrs(inputlines)

    gamma, epsilon = calculate_gamma_epsilon(numstrs)
    ogr = calculate_ogr(numstrs)
    csr = calculate_csr(numstrs)

    return gamma * epsilon, ogr * csr
