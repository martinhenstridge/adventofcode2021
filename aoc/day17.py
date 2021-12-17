import re
from . import util


def get_target_area(lines):
    for line in lines:
        if line:
            m = re.fullmatch(r"target area: x=(\d+)\.\.(\d+), y=(\-\d+)\.\.(\-\d+)", line)
            return (int(m[1]), int(m[2])), (int(m[3]), int(m[4]))


def find_peak(v):
    return v * (v + 1) // 2


def find_vx_min(goal):
    x = 0
    v = 0
    while x < goal:
        x += v
        v += 1
    return v - 1


def find_x_at_step(step, vx):
    if step >= vx:
        return find_peak(vx)
    hi = vx
    lo = 1 + vx - step
    return ((hi + lo) * step) // 2


def find_steps_within_targety(targety, vy):
    step = 0
    y = 0
    v = vy

    # If initially moving upwards, skip to the point where we get back to y=0
    # moving downwards. It takes vy steps moving upwards to decelerate to v=0,
    # one step moving only in the x-direction at the peak where v=0, then vy
    # more steps accelerating downwards to get back to y=0. The velocity for
    # the next step after we get back to y=0 is vy+1, but facing downwards.
    if vy > 0:
        step = 1 + 2 * vy
        v = -(vy + 1)

    steps = []
    while y >= targety[0]:
        if y <= targety[1]:
            steps.append(step)
        y += v
        v -= 1
        step += 1
    return steps


def run():
    inputlines = util.get_input_lines("17.txt")
    targetx, targety = get_target_area(inputlines)

    vy_min = targety[0]
    vy_max = abs(targety[0]) - 1

    vx_min = find_vx_min(targetx[0])
    vx_max = targetx[1]

    peak = find_peak(vy_max)

    count = 0
    for vy in range(vy_min, vy_max + 1):
        if steps := find_steps_within_targety(targety, vy):
            for vx in range(vx_min, vx_max + 1):
                for step in steps:
                    x = find_x_at_step(step, vx)
                    if targetx[0] <= x <= targetx[1]:
                        count += 1
                        break

    return peak, count
