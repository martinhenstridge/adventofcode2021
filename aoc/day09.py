from . import util


class HeightMap:
    def __init__(self, lines):
        self._map = [[int(h) for h in line] for line in lines if line]
        self.rows = len(self._map)
        self.cols = len(self._map[0])

    def __getitem__(self, i):
        return self._map[i]

    def neighbours(self, row, col):
        for drow, dcol in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
            nrow = row + drow
            ncol = col + dcol
            if nrow < 0 or nrow >= self.rows:
                continue
            if ncol < 0 or ncol >= self.cols:
                continue
            yield nrow, ncol


def find_low_points(heightmap):
    low_points = []
    for row in range(heightmap.rows):
        for col in range(heightmap.cols):
            height = heightmap[row][col]
            if all(
                height < heightmap[r][c]
                for r, c in heightmap.neighbours(row, col)
            ):
                low_points.append((row, col))
    return low_points


def find_basin_size(heightmap, low_point):
    basin = {low_point}

    row, col = low_point
    edge = set(heightmap.neighbours(row, col))
    while edge:
        this = edge.pop()
        row, col = this
        if heightmap[row][col] == 9:
            continue
        basin.add(this)
        for neighbour in heightmap.neighbours(row, col):
            if neighbour not in basin:
                edge.add(neighbour)

    return len(basin)


def run():
    inputlines = util.get_input_lines("09.txt")
    heightmap = HeightMap(inputlines)

    low_points = find_low_points(heightmap)
    risk_levels = [1 + heightmap[r][c] for r, c in low_points]
    basin_sizes = sorted(
        (find_basin_size(heightmap, lp) for lp in low_points),
        reverse=True,
    )

    return sum(risk_levels), util.product(basin_sizes[:3])
