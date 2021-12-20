from collections import defaultdict
from . import util


def get_algorithm_image(lines):
    lineiter = iter(lines)

    algorithm = None
    image = defaultdict(lambda: "0")

    while line := next(lineiter):
        algorithm = ["1" if c == "#" else "0" for c in line]

    row = 0
    while line := next(lineiter):
        for col, char in enumerate(line):
            image[row, col] = "1" if char == "#" else "0"
        row += 1

    return algorithm, image, (0, row)


def get_neighbours(pixel):
    row, col = pixel
    return [
        (row-1, col-1), (row-1, col), (row-1, col+1),
        (row,   col-1), (row,   col), (row,   col+1),
        (row+1, col-1), (row+1, col), (row+1, col+1),
    ]


def enhance(algorithm, image, extent, background):
    enhanced = defaultdict(background)
    extent = (extent[0] - 1, extent[1] + 1)

    for row in range(extent[0], extent[1]):
        for col in range(extent[0], extent[1]):
            pixel = (row, col)
            lookup = int("".join(image[n] for n in get_neighbours(pixel)), 2)
            enhanced[pixel] = algorithm[lookup]

    return enhanced, extent


# The infinite background flips colour every time the image is enhanced, so the
# default value for those pixels not explicitly stored in the original image
# also needs to flip on each iteration.
BACKGROUND = [lambda: "1", lambda: "0"]

def run():
    inputlines = util.get_input_lines("20.txt")
    algorithm, image, extent = get_algorithm_image(inputlines)

    for i in range(2):
        image, extent = enhance(algorithm, image, extent, BACKGROUND[i % 2])
    count2 = sum(1 for pixel in image.values() if pixel == "1")

    for i in range(2, 50):
        image, extent = enhance(algorithm, image, extent, BACKGROUND[i % 2])
    count50 = sum(1 for pixel in image.values() if pixel == "1")

    return count2, count50
