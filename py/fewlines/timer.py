import time
from contextlib import contextmanager

import fewlines.metrics as fm

@contextmanager
def Timer(name):
    start_time = time.monotonic_ns()
    try:
        yield
    finally:
        end_time = time.monotonic_ns()
        elapsed_time = end_time - start_time
        # Append the measurement to the list of times for this name
        fm.add(name, (elapsed_time / 1000000))
