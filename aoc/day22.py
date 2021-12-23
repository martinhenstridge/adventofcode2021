import re
from typing import NamedTuple
from . import util


class Cuboid(NamedTuple):
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    @property
    def count(self):
        return (
            (1 + self.xmax - self.xmin)
            * (1 + self.ymax - self.ymin)
            * (1 + self.zmax - self.zmin)
        )

    def within(self, lo, hi):
        if self.xmin < lo or self.xmin > hi:
            return False
        if self.xmax < lo or self.xmax > hi:
            return False
        if self.ymin < lo or self.ymin > hi:
            return False
        if self.ymax < lo or self.ymax > hi:
            return False
        if self.zmin < lo or self.zmin > hi:
            return False
        if self.zmax < lo or self.zmax > hi:
            return False
        return True

    def overlaps(self, other):
        if self.xmin > other.xmax:
             return False
        if self.xmax < other.xmin:
            return False
        if self.ymin > other.ymax:
            return False
        if self.ymax < other.ymin:
            return False
        if self.zmin > other.zmax:
            return False
        if self.zmax < other.zmin:
            return False
        return True

    def split(self, other):
        """Split `other` into cuboids not overlapping `self`"""
        missing = set()
        hitting = {other}
        for imin, imax in [(0, 1), (2, 3), (4, 5)]:
            candidates = hitting.copy()
            hitting = set()
            for candidate in candidates:
                _hitting, _missing = self._split_axis(candidate, imin, imax)
                hitting.update(_hitting)
                missing.update(_missing)
        return missing

    def _split_axis(self, other, imin, imax):
        """Split `other` along a single axis of `self`"""
        if self[imin] > other[imax]:
            # missing entirely on right side
            return [], [other]

        if self[imax] < other[imin]:
            # missing entirely on left side
            return [], [other]

        if self[imin] <= other[imin] and self[imax] >= other[imax]:
            # fully subsuming
            return [other], []

        if self[imin] <= other[imin]:
            # self[imax] is in middle of other
            hitting = [other._replace(**{self._fields[imax]: self[imax]})]
            missing = [other._replace(**{self._fields[imin]: self[imax] + 1})]
            return hitting, missing

        if self[imax] >= other[imax]:
            # self[imin] is in middle of other
            hitting = [other._replace(**{self._fields[imin]: self[imin]})]
            missing = [other._replace(**{self._fields[imax]: self[imin] - 1})]
            return hitting, missing

        # self[imin] and self[imax] are both in middle of other
        hitting = [other._replace(**{self._fields[imin]: self[imin], self._fields[imax]: self[imax]})]
        missing = [
            other._replace(**{self._fields[imax]: self[imin] - 1}),
            other._replace(**{self._fields[imin]: self[imax] + 1}),
        ]
        return hitting, missing


def get_reboot_steps(lines):
    regex = (
        r"(on|off)"
        r" x=(\-?\d+)\.\.(\-?\d+)"
        r",y=(\-?\d+)\.\.(\-?\d+)"
        r",z=(\-?\d+)\.\.(\-?\d+)"
    )
    steps = []
    for line in lines:
        if match := re.fullmatch(regex, line):
            turnon = (match[1] == "on")
            cuboid = Cuboid(
                int(match[2]),
                int(match[3]),
                int(match[4]),
                int(match[5]),
                int(match[6]),
                int(match[7]),
            )
            steps.append((turnon, cuboid))
    return steps


def reboot(steps):
    cuboids = set()

    for turnon, cuboid in steps:
        updated = set()
        for existing in cuboids:
            if not cuboid.overlaps(existing):
                updated.add(existing)
            else:
                for new in cuboid.split(existing):
                    updated.add(new)
        if turnon:
            updated.add(cuboid)
        cuboids = updated

    return sum(c.count for c in cuboids)


def run():
    inputlines = util.get_input_lines("22.txt")
    steps = get_reboot_steps(inputlines)

    init_count = reboot([s for s in steps if s[1].within(-50, 50)])
    full_count = reboot(steps)

    return init_count, full_count
