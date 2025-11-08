# data_utils/decorators.py

import time
import functools
import warnings
from threading import Lock

def rate_limit(calls_per_minute=60):
    """Limit calls per minute."""
    def decorator(func):
        last_calls = []
        lock = Lock()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                now = time.time()
                # Clean up old calls
                while last_calls and (now - last_calls[0]) > 60:
                    last_calls.pop(0)
                if len(last_calls) >= calls_per_minute:
                    raise Exception("Rate limit exceeded")
                last_calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def deprecated(message="This function is deprecated."):
    """Warn when function is deprecated."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def audit_trail(func):
    """Log all function calls with timestamp to audit.log."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with open("audit.log", "a", encoding="utf-8") as log:
            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Called {func.__name__}\n")
        return func(*args, **kwargs)
    return wrapper
