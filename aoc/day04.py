from . import util


class Board:
    def __init__(self):
        self.rows = []
        self.cols = [set() for _ in range(5)]
        self.last = None

    def grow(self, line):
        self.rows.append(set(line))
        for i, n in enumerate(line):
            self.cols[i].add(n)

    def play(self, order):
        for idx, number in enumerate(order):
            win = self._mark(number)
            if win:
                return idx, self._score()

    def _mark(self, number):
        for row in self.rows:
            if number in row:
                row.discard(number)
                if not row:
                    self.last = number
                break  # Can only be in one row
        for col in self.cols:
            if number in col:
                col.discard(number)
                if not col:
                    self.last = number
                break  # Can only be in one column
        return self.last is not None

    def _score(self):
        return self.last * sum(n for row in self.rows for n in row)


def get_bingo_order_boards(lines):
    order = None
    board = None
    boards = []

    for line in lines:
        # First line: parse order
        if order is None:
            order = [int(n) for n in line.split(",")]
            continue

        # Blank line: store current board and get ready for next one
        if not line:
            if board is not None:
                boards.append(board)
            board = Board()
            continue

        # Other: add line to current board
        board.grow([int(n) for n in line.split()])

    return order, boards


def run():
    inputlines = util.get_input_lines("04.txt")
    order, boards = get_bingo_order_boards(inputlines)

    # Play all boards to completion, sort by how quickly they finish.
    results = sorted(board.play(order) for board in boards)

    return results[0][1], results[-1][1]
