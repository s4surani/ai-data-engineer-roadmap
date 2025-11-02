# while_loops.py - Understanding While Loops

import time
import random

# Basic while loop
print("Countdown Timer:")
count = 5
while count > 0:
    print(f"  {count}...")
    count -= 1
    time.sleep(0.5)
print("  🚀 Liftoff!\n")

print("="*60 + "\n")

# While loop with user input simulation
print("API Retry Logic Simulation:")

max_retries = 5
retry_count = 0
success = False

while retry_count < max_retries and not success:
    retry_count += 1
    print(f"  Attempt {retry_count}/{max_retries}...")
    
    # Simulate API call (random success/failure)
    api_response = random.choice([True, False, False])  # 33% success rate
    
    if api_response:
        print(f"  ✅ Success on attempt {retry_count}!")
        success = True
    else:
        print(f"  ❌ Failed. Retrying in 2 seconds...")
        time.sleep(2)

if not success:
    print(f"  ⚠️  Failed after {max_retries} attempts")

print("\n" + "="*60 + "\n")

# Processing data until condition met
print("Data Processing Until Target:")

total_processed = 0
target = 1000
batch_size = 150

while total_processed < target:
    # Process batch
    total_processed += batch_size
    progress = (total_processed / target) * 100
    
    print(f"  Processed: {total_processed}/{target} ({progress:.1f}%)")
    
    if total_processed >= target:
        print(f"  ✅ Target reached!")
        break

print("\n" + "="*60 + "\n")

# Infinite loop with break (monitoring simulation)
print("System Monitoring (Press Ctrl+C to stop):")
print("Monitoring for 10 seconds...\n")

start_time = time.time()
check_count = 0

while True:
    check_count += 1
    elapsed = time.time() - start_time
    
    # Simulate system check
    cpu_usage = random.randint(20, 80)
    memory_usage = random.randint(40, 90)
    
    print(f"  Check #{check_count}: CPU: {cpu_usage}%, Memory: {memory_usage}%")
    
    # Alert on high usage
    if cpu_usage > 70 or memory_usage > 85:
        print(f"    ⚠️  High resource usage detected!")
    
    # Stop after 10 seconds
    if elapsed > 10:
        print(f"\n  Monitoring complete. Total checks: {check_count}")
        break
    
    time.sleep(2)