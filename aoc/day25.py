from . import util


def get_cucumbers(lines):
    return [list(line) for line in lines if line]


def move(cucumbers):
    moved = False

    can_move_east = []
    for r in range(len(cucumbers)):
        for c in range(len(cucumbers[r])):
            if cucumbers[r][c-1] == ">" and cucumbers[r][c] == ".":
                can_move_east.append((r, c))
    for r, c in can_move_east:
        cucumbers[r][c] = ">"
        cucumbers[r][c-1] = "."
        moved = True

    can_move_south = []
    for r in range(len(cucumbers)):
        for c in range(len(cucumbers[r])):
            if cucumbers[r-1][c] == "v" and cucumbers[r][c] == ".":
                can_move_south.append((r, c))
    for r, c in can_move_south:
        cucumbers[r][c] = "v"
        cucumbers[r-1][c] = "."
        moved = True

    return moved


def run():
    inputlines = util.get_input_lines("25.txt")
    cucumbers = get_cucumbers(inputlines)

    count = 0
    while True:
        moved = move(cucumbers)
        count += 1
        if not moved:
            break

    return count, None
