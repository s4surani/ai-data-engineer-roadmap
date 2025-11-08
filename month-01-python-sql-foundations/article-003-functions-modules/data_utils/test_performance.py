# tests/test_performance.py

import time
import tracemalloc
from data_utils.transformers import clean_text

def time_function(func, *args, **kwargs):
    """Return function result and execution time."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return result, end - start

def memory_usage(func, *args, **kwargs):
    """Return peak memory usage during function call."""
    tracemalloc.start()
    func(*args, **kwargs)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return current, peak

def test_clean_text_performance():
    sample = "Hello, World! #Test 123"
    _, exec_time = time_function(clean_text, sample)
    assert exec_time < 0.1  # Should be fast

def test_clean_text_memory():
    sample = "Hello, World! #Test 123"
    _, peak = memory_usage(clean_text, sample)
    assert peak < 100000  # <100KB acceptable for this function
