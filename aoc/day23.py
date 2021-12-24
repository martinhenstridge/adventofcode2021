from . import util


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


def is_blocker(state, which, room, i):
    return not all(state[r] in [".", which] for r in room[i + 1:])


def contains_wrong(state, which, room):
    return not all(state[r] in [".", which] for r in room)


def get_path(state, src, dst):
    return state[src + 1:dst] if src < dst else state[dst + 1:src]


def get_moves(rooms, doorways, state):
    # First, check for moves within rooms.
    for which, room in rooms.items():
        for i, r in enumerate(room):
            x = state[r]
            if x == ".":
                continue

            # Move towards hallway if in wrong room or a blocker
            if i > 0:
                target = room[i - 1]
                if state[target] != ".":
                    continue
                if x != which or is_blocker(state, which, room, i):
                    yield move(state, r, target), COST[x]
                    return

            # Move away from hallway if in right room and not a blocker
            if i < len(room) - 1:
                target = room[i + 1]
                if state[target] != ".":
                    continue
                if x == which and not is_blocker(state, which, room, i):
                    yield move(state, r, target), COST[x]
                    return

    # If in hallway, move into correct room if possible
    for h in range(11):
        x = state[h]
        if x == ".":
            continue

        target = rooms[x][0]
        if state[target] != ".":
            continue
        if contains_wrong(state, x, rooms[x]):
            continue

        # Check for obstructions on path to doorway
        path = get_path(state, h, doorways[state[h]])
        if all(p == "." for p in path):
            yield move(state, h, target), COST[x] * (len(path) + 2)
            return

    # If no other options, move from the wrong room into the hallway
    for which, room in rooms.items():
        x = state[room[0]]
        if x == ".":
            continue
        if x == which and not is_blocker(state, which, room, 0):
            continue

        doorway = doorways[which]
        for h in range(doorway, -1, -1):
            if h in doorways.values():
                continue
            if state[h] != ".":
                break
            yield move(state, room[0], h), COST[x] * (doorway - h + 1)
        for h in range(doorway, 11, +1):
            if h in doorways.values():
                continue
            if state[h] != ".":
                break
            yield move(state, room[0], h), COST[x] * (h - doorway + 1)


def solve(state, rooms, doorways):
    states = {state: 0}

    q = [state]
    while q:
        state0 = q.pop()
        cost0 = states[state0]
        for state1, cost1 in get_moves(rooms, doorways, state0):
            if state1 in states and cost0 + cost1 >= states[state1]:
                continue
            states[state1] = cost0 + cost1
            q.append(state1)

    return states


def run():
    inputlines = util.get_input_lines("23.txt")

    state, rooms, doorways = get_situation(inputlines)
    states = solve(state, rooms, doorways)
    cost1 = states["...........ABCDABCD"]

    state, rooms, doorways = get_situation(
        [
            *inputlines[:3],
            "  #D#C#B#A#",
            "  #D#B#A#C#",
            *inputlines[3:],
        ]
    )
    states = solve(state, rooms, doorways)
    cost2 = states["...........ABCDABCDABCDABCD"]

    return cost1, cost2
