from . import util


def get_timers(lines):
    timers = [0] * 9
    for line in lines:
        if line:
            for t in line.split(","):
                timers[int(t)] += 1
    return timers


def tick(timers):
    # All timers shift down (i.e. decrement) by 1 on each tick, wrapping back
    # around from 0 to 8 (i.e. creating new fish).
    result = timers[1:] + timers[:1]

    # Additionally, timers reaching 0 reset to 6.
    result[6] += timers[0]

    return result


def run():
    inputlines = util.get_input_lines("06.txt")
    timers = get_timers(inputlines)

    for _ in range(80):
        timers = tick(timers)
    count80 = sum(timers)

    for _ in range(256 - 80):
        timers = tick(timers)
    count256 = sum(timers)

    return count80, count256
