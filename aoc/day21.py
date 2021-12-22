from collections import defaultdict
from . import util


def get_starting_positions(lines):
    return [int(line[-1]) for line in lines if line]


def roll3_deterministic():
    value = 1
    while True:
        if value < 98:
            # (first + last) * pairs
            yield (value + 1) * 3
            value += 3
        elif value == 98:
            # 98, 99, 100
            yield 297
            value = 1
        elif value == 99:
            # 99, 100, 1
            yield 200
            value = 2
        if value == 100:
            # 100, 1, 2
            yield 103
            value = 3


ROLL3_QUANTUM = {
    # 1 1 1
    3: 1,

    # 1 1 2
    # 1 2 1
    # 2 1 1
    4: 3,

    # 1 1 3
    # 1 3 1
    # 3 1 1
    # 1 2 2
    # 2 1 2
    # 2 2 1
    5: 6,

    # 1 2 3
    # 1 3 2
    # 2 1 3
    # 2 3 1
    # 3 1 2
    # 3 2 1
    # 2 2 2
    6: 7,

    # 1 3 3
    # 3 1 3
    # 3 3 1
    # 2 2 3
    # 2 3 2
    # 3 2 2
    7: 6,

    # 2 2 3
    # 2 3 2
    # 3 2 2
    8: 3,

    # 3 3 3
    9: 1,
}


def play_deterministic(starting):
    positions = starting.copy()
    scores = [0, 0]

    roll3 = roll3_deterministic()
    rolls = 0

    player = 0
    winner = None
    while winner is None:
        positions[player] = (positions[player] + next(roll3) - 1) % 10 + 1
        rolls += 3

        scores[player] += positions[player]
        if scores[player] >= 1000:
            winner = player

        player = 1 - player

    return scores[player], rolls


def play_quantum(starting):
    ongoing = defaultdict(int)
    ongoing[0, starting[0], starting[1], 0, 0] += 1

    wins = [0, 0]
    positions = [None, None]
    scores = [None, None]

    while ongoing:
        state, count = ongoing.popitem()

        for total, times in ROLL3_QUANTUM.items():
            player = state[0]
            positions[0] = state[1]
            positions[1] = state[2]
            scores[0] = state[3]
            scores[1] = state[4]

            positions[player] = (positions[player] + total - 1) % 10 + 1
            scores[player] += positions[player]

            if scores[player] >= 21:
                wins[player] += count * times
            else:
                ongoing[
                    1 - player,
                    positions[0],
                    positions[1],
                    scores[0],
                    scores[1],
                ] += count * times
    return wins


def run():
    inputlines = util.get_input_lines("21.txt")
    positions = get_starting_positions(inputlines)

    losing_score, num_rolls = play_deterministic(positions)
    win_counts = play_quantum(positions)

    return losing_score * num_rolls, max(win_counts)
