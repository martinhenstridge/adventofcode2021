import math
import heapq
from enum import IntEnum
from typing import NamedTuple
from . import util

LINES = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""".splitlines()


class State(IntEnum):
    INIT = 0
    HALL = 1
    ROOM = 2


class Position(NamedTuple):
    row: int
    col: int


class Amphipod(NamedTuple):
    which: str
    where: Position
    state: State = State.INIT


def get_situation(lines):
    amphipods = []
    hallway = []
    rooms = {"A": [], "B": [], "C": [], "D": []}

    for row, line in enumerate(lines):
        room = "A"
        for col, char in enumerate(line):
            if char == "#" or char == " ":
                continue
            position = Position(row, col)
            if char == ".":
                hallway.append(position)
            else:
                amphipods.append(Amphipod(char, position))
                rooms[room].append(position)
                room = chr(ord(room) + 1)
    
    # Filter out hallway locations immediately outside rooms.
    outside = set(p.col for ps in rooms.values() for p in ps)
    hallway = [p for p in hallway if p.col not in outside]

    return amphipods, hallway, rooms


COST = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def manhattan(p1, p2):
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)


def cost(amphipod, target):
    return COST[amphipod.which] * manhattan(amphipod.where, target)


def get_valid_moves_into_hallway(hallway, amphipods, amphipod):
    assert amphipod.state is State.INIT

    # Check if blocked from exiting room
    for other in amphipods:
        if other.where.col == amphipod.where.col and other.where.row < amphipod.where.row:
            return

    # Check for non-blocked positions in hallway
    others = [a.where.col for a in amphipods if a is not amphipod and a.state is State.HALL]
    for position in hallway:
        lo = min(position.col, amphipod.where.col)
        hi = max(position.col, amphipod.where.col)
        if all(col < lo or col > hi for col in others):
            yield State.HALL, position


def get_valid_moves_into_room(rooms, amphipods, amphipod):
    assert amphipod.state is State.HALL

    room = sorted(rooms[amphipod.which], key=lambda p: -p.row)
    goal = room[0]

    # Check target room for occupants
    for other in amphipods:
       if other.where in room:
           # Cannot enter room with non-matching amphipod
           if other.which is not amphipod.which:
               return
           # Room is already occupied by the other matching amphipod
           goal = room[1]
           break

    # Check hallway leading up to room is clear
    others = [a.where.col for a in amphipods if a is not amphipod and a.state is State.HALL]
    lo = min(room[0].col, amphipod.where.col)
    hi = max(room[0].col, amphipod.where.col)
    if all(col < lo or col > hi for col in others):
        yield State.ROOM, goal


def get_valid_moves(hallway, rooms, amphipods, amphipod):
    if amphipod.state is State.INIT:
        yield from get_valid_moves_into_hallway(hallway, amphipods, amphipod)
    elif amphipod.state is State.HALL:
        yield from get_valid_moves_into_room(rooms, amphipods, amphipod)
    elif amphipod.state is State.ROOM:
        pass


def dump(amphipods):
    canvas = [["."] * 13 for _ in range(5)]
    for amphipod in amphipods:
        canvas[amphipod.where.row][amphipod.where.col] = amphipod.which
    for line in canvas:
        print(*line)
        

def solve(starting, hallway, rooms):
    lowest = math.inf

    pending = []
    heapq.heappush(pending, (0, starting.copy()))

    while pending:
        current_cost, current_amphipods = heapq.heappop(pending)
        if current_cost > 10000:
            break

        #print("====")
        #dump(current_amphipods)
        #print(current_cost)
        #print("====")
        for i, amphipod in enumerate(current_amphipods):
            #print("considering", amphipod)
            for state, position in get_valid_moves(hallway, rooms, current_amphipods, amphipod):
                total_cost = current_cost + cost(amphipod, position)

                amphipods = current_amphipods.copy()
                amphipods[i] = amphipod._replace(where=position, state=state)

                if all(a.state is State.ROOM for a in amphipods):
                    print("COMPLETE")
                    dump(amphipods)
                    print(total_cost)
                    if total_cost < lowest:
                        lowest = total_cost
                elif total_cost < lowest:
                    heapq.heappush(pending, (total_cost, amphipods))
                    #dump(amphipods)
                    #print(total_cost)
            #input()
        #for _cost, amphipods in pending:
        #    dump(amphipods)
        #    print(_cost)
        #    input()
    return lowest


def run():
    inputlines = util.get_input_lines("23.txt")
    inputlines = LINES
    amphipods, hallway, rooms = get_situation(inputlines)

    energy = solve(amphipods, hallway, rooms)

    return energy, None
