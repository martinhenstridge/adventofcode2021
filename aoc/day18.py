from . import util


class Regular:
    __slots__ = ("parent", "value")

    def __init__(self, parent, value):
        self.parent = parent
        self.value = value

    def clone(self):
        return Regular(None, self.value)

    def magnitude(self):
        return self.value

    def split(self):
        pair = Pair(self.parent)
        lvalue = self.value // 2
        rvalue = self.value - lvalue
        pair.lchild = Regular(pair, lvalue)
        pair.rchild = Regular(pair, rvalue)

        if self is self.parent.lchild:
            self.parent.lchild = pair
        elif self is self.parent.rchild:
            self.parent.rchild = pair


class Pair:
    __slots__ = ("parent", "lchild", "rchild")

    def __init__(self, parent):
        self.parent = parent
        self.lchild = None
        self.rchild = None

    def __add__(self, other):
        result = Pair(None)
        result.lchild = self.clone()
        result.rchild = other.clone()
        result.lchild.parent = result
        result.rchild.parent = result
        while True:
            reduced = result.reduce()
            if reduced:
                return result

    def clone(self):
        result = Pair(None)
        result.lchild = self.lchild.clone()
        result.rchild = self.rchild.clone()
        result.lchild.parent = result
        result.rchild.parent = result
        return result

    def magnitude(self):
        lmag = 3 * self.lchild.magnitude()
        rmag = 2 * self.rchild.magnitude()
        return lmag + rmag

    def walk_pairs(self, depth=0):
        yield depth, self
        if isinstance(self.lchild, Pair):
            yield from self.lchild.walk_pairs(depth + 1)
        if isinstance(self.rchild, Pair):
            yield from self.rchild.walk_pairs(depth + 1)

    def walk_regulars(self):
        if isinstance(self.lchild, Regular):
            yield self.lchild
        else:
            yield from self.lchild.walk_regulars()
        if isinstance(self.rchild, Regular):
            yield self.rchild
        else:
            yield from self.rchild.walk_regulars()

    def reduce(self):
        reduced = True

        # Explode every pair that needs exploding in a single pass. This is safe
        # because the operation only reduces nesting, so can never trigger more
        # explosions. All explosions are also always handled before splits.
        for depth, pair in self.walk_pairs():
            if depth == 4:
                pair.explode()
                reduced = False

        # Splitting increases nesting and so can trigger an explosion, so we
        # need to break out as soon as we've performed a split.
        for regular in self.walk_regulars():
            if regular.value >= 10:
                regular.split()
                return False

        return reduced

    def find_left_regular(self):
        node = self
        while node.parent and node is node.parent.lchild:
            node = node.parent
        if not node.parent:
            return None
        node = node.parent.lchild
        while not isinstance(node, Regular):
            node = node.rchild
        return node

    def find_right_regular(self):
        node = self
        while node.parent and node is node.parent.rchild:
            node = node.parent
        if not node.parent:
            return None
        node = node.parent.rchild
        while not isinstance(node, Regular):
            node = node.lchild
        return node

    def explode(self):
        # Add left child value to the next regular number on the left.
        neighbour = self.find_left_regular()
        if neighbour is not None:
            neighbour.value += self.lchild.value

        # Add right child value to the next regular number on the right.
        neighbour = self.find_right_regular()
        if neighbour is not None:
            neighbour.value += self.rchild.value

        # Replace exploding pair with regular number 0.
        zero = Regular(self.parent, 0)
        if self is self.parent.lchild:
            self.parent.lchild = zero
        elif self is self.parent.rchild:
            self.parent.rchild = zero

    @classmethod
    def from_string(cls, string, parent=None):
        this = cls(parent)
        lstring, rstring = cls.split_string(string)

        if len(lstring) == 1:
            this.lchild = Regular(this, int(lstring))
        else:
            this.lchild = cls.from_string(lstring, this)

        if len(rstring) == 1:
            this.rchild = Regular(this, int(rstring))
        else:
            this.rchild = cls.from_string(rstring, this)

        return this

    @staticmethod
    def split_string(string):
        stripped = string[1 : -1]
        depth = 0
        for i, c in enumerate(stripped):
            if c == ",":
                if depth == 0:
                    return stripped[:i], stripped[i + 1:]
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1


def get_numbers(lines):
    return [Pair.from_string(line) for line in lines if line]


def run():
    inputlines = util.get_input_lines("18.txt")
    numbers = get_numbers(inputlines)

    total = numbers[0]
    for number in numbers[1:]:
        total += number

    largest = 0
    for i, inum in enumerate(numbers):
        for j, jnum in enumerate(numbers):
            if i != j:
                magnitude = (inum + jnum).magnitude()
                if magnitude > largest:
                    largest = magnitude

    return total.magnitude(), largest
