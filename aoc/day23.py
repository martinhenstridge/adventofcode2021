import math
import heapq
from . import util

LINES = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""".splitlines()


COST = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def get_situation(lines):
    state = []
    rooms = {"A": [], "B": [], "C": [], "D": []}
    doorways = {}

    idx = 0
    for row, line in enumerate(lines):
        room = "A"
        for col, char in enumerate(line):
            if char == "#" or char == " ":
                continue
            state.append(char)
            if char == ".":
                if lines[row + 1][col] != "#":
                    doorways[room] = idx
                    room = chr(ord(room) + 1)
            else:
                rooms[room].append(idx)
                room = chr(ord(room) + 1)
            idx += 1
    
    return "".join(state), rooms, doorways


def move(state, src, dst):
    _state = list(state)
    _state[dst] = state[src]
    _state[src] = "."
    return "".join(_state)


def get_moves(rooms, doorways, state):
    for which, room in rooms.items():
        outer = room[0]
        inner = room[1]

        # If in wrong room, move towards the door if possible
        if state[inner] != "." and state[inner] != which and state[outer] == ".":
            yield move(state, inner, outer), COST[state[inner]]
            return

        # If in right room, move away from the door if possible
        if state[outer] != "." and state[outer] == which and state[inner] == ".":
            yield move(state, outer, inner), COST[state[outer]]
            return

    # If in hallway, move into correct room if possible
    for h in range(11):
        if state[h] == ".":
            continue
        amphipod = state[h]
        goal = rooms[amphipod][0]
        if state[goal] != ".":
            continue
        doorway = doorways[state[h]]
        path = state[h+1:doorway] if h < doorway else state[doorway+1:h]
        if all(p == "." for p in path):
            yield move(state, h, goal), COST[amphipod] * (len(path) + 2)
            return

    # If no other options, move from the wrong room into the hallway
    for which, room in rooms.items():
        outer = room[0]
        if state[outer] == ".":
            continue
        ...


def dump(state):
    print(*state[:11])
    print(f"    {state[11]}   {state[12]}   {state[13]}   {state[14]}")
    print(f"    {state[15]}   {state[16]}   {state[17]}   {state[18]}")


def run():
    inputlines = util.get_input_lines("23.txt")
    inputlines = LINES
    state, rooms, doorways = get_situation(inputlines)

    #print(state)
    #for k, v in rooms.items():
    #    print(k, v)
    #print(doorways)
    #dump(state)

    state = "..........A..CDABCD"
    dump(state)
    for move, cost in get_moves(rooms, doorways, state):
        dump(move)
        print(cost)

    return None, None
