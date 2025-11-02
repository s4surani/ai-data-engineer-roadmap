# decorators.py - Useful decorators for data engineering

import time
import functools
from datetime import datetime


def timer(func):
    """
    Decorator to measure function execution time
    
    Usage:
        @timer
        def my_function():
            # code here
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"⏱️  {func.__name__} took {duration:.4f} seconds")
        
        return result
    return wrapper


def logger(func):
    """
    Decorator to log function calls
    
    Usage:
        @logger
        def my_function(x, y):
            return x + y
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"📝 [{timestamp}] Calling {func.__name__}")
        print(f"   Args: {args}")
        print(f"   Kwargs: {kwargs}")
        
        result = func(*args, **kwargs)
        
        print(f"   Result: {result}")
        return result
    return wrapper


def retry(max_attempts=3, delay=1):
    """
    Decorator to retry function on failure
    
    Usage:
        @retry(max_attempts=5, delay=2)
        def api_call():
            # code that might fail
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        print(f"❌ Failed after {max_attempts} attempts")
                        raise
                    print(f"⚠️  Attempt {attempts} failed: {e}")
                    print(f"   Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator


def validate_types(**type_checks):
    """
    Decorator to validate function argument types
    
    Usage:
        @validate_types(price=float, quantity=int)
        def calculate_revenue(price, quantity):
            return price * quantity
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate types
            for param_name, expected_type in type_checks.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Parameter '{param_name}' must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def cache_result(func):
    """
    Decorator to cache function results
    
    Usage:
        @cache_result
        def expensive_calculation(x):
            # expensive operation
            return result
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"💾 Using cached result for {func.__name__}{args}")
            return cache[args]
        
        result = func(*args)
        cache[args] = result
        return result
    return wrapper


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("🎨 DECORATOR DEMONSTRATIONS")
    print("="*70 + "\n")
    
    # Timer decorator
    @timer
    def process_large_dataset():
        """Simulate processing"""
        time.sleep(2)
        return "Processed 1M records"
    
    print("1. Timer Decorator:")
    result = process_large_dataset()
    print(f"   Result: {result}\n")
    
    # Logger decorator
    @logger
    def calculate_revenue(price, quantity):
        """Calculate revenue"""
        return price * quantity
    
    print("2. Logger Decorator:")
    revenue = calculate_revenue(1000, 50)
    print()
    
    # Retry decorator
    @retry(max_attempts=3, delay=1)
    def unreliable_api_call():
        """Simulate unreliable API"""
        import random
        if random.random() < 0.7:  # 70% failure rate
            raise Exception("API timeout")
        return "Success!"
    
    print("3. Retry Decorator:")
    try:
        result = unreliable_api_call()
        print(f"   {result}\n")
    except Exception as e:
        print(f"   Final failure: {e}\n")
    
    # Type validation decorator
    @validate_types(price=float, quantity=int)
    def calculate_total(price, quantity):
        """Calculate total with type checking"""
        return price * quantity
    
    print("4. Type Validation Decorator:")
    try:
        total = calculate_total(100.0, 5)
        print(f"   ✅ Valid call: {total}")
        
        total = calculate_total("100", 5)  # This will fail
    except TypeError as e:
        print(f"   ❌ Invalid call: {e}\n")
    
    # Cache decorator
    @cache_result
    @timer
    def fibonacci(n):
        """Calculate Fibonacci number"""
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print("5. Cache Decorator:")
    print(f"   First call: fib(10) = {fibonacci(10)}")
    print(f"   Second call: fib(10) = {fibonacci(10)}")  # Uses cache
    
    print("\n" + "="*70)
    print("✅ DEMONSTRATIONS COMPLETE")
    print("="*70)