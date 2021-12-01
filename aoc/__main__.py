import sys
import time
from . import DAYS


def run(day, solver, solutions):
    start = time.monotonic()
    results = solver.run()
    end = time.monotonic()

    print()
    for idx, result in enumerate(results):
        print(f"[{day}/{idx+1}] {result}")
    print(f"{1000 * (end - start):.3f}ms")
    assert results == solutions


if len(sys.argv) > 1:
    day = sys.argv[1]
    run(day, *DAYS[day])
else:
    for day in DAYS:
        run(day, *DAYS[day])
