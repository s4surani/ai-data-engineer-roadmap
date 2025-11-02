# list_comprehensions.py - Mastering List Comprehensions

# Traditional way vs List Comprehension
print("Traditional Loop:")
prices = [100, 200, 300, 400, 500]
discounted_prices = []
for price in prices:
    discounted_prices.append(price * 0.9)
print(f"Discounted: {discounted_prices}\n")

print("List Comprehension (same result):")
discounted_prices = [price * 0.9 for price in prices]
print(f"Discounted: {discounted_prices}\n")

print("="*60 + "\n")

# With conditional filtering
sales_data = [45000, 52000, 38000, 61000, 48000, 72000, 35000]

# Get only high-performing months (>50k)
high_sales = [sale for sale in sales_data if sale > 50000]
print(f"High Sales Months: {high_sales}")

# Get low-performing months with warning
low_sales = [f"⚠️  ₹{sale:,}" for sale in sales_data if sale < 40000]
print(f"Low Sales Months: {low_sales}\n")

print("="*60 + "\n")

# Dictionary comprehension
products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor']
prices = [75000, 500, 1500, 25000]

# Create product-price dictionary
product_catalog = {product: price for product, price in zip(products, prices)}
print("Product Catalog:")
for product, price in product_catalog.items():
    print(f"  {product}: ₹{price:,}")

print("\n" + "="*60 + "\n")

# Nested list comprehension (matrix operations)
regions = ['North', 'South', 'East', 'West']
products = ['Laptop', 'Mouse', 'Keyboard']

# Generate all region-product combinations
combinations = [f"{region}-{product}" for region in regions for product in products]
print(f"Total Combinations: {len(combinations)}")
print("First 5 combinations:")
for combo in combinations[:5]:
    print(f"  {combo}")

print("\n" + "="*60 + "\n")

# Real-world example: Data cleaning
raw_customer_ids = ['C001', 'c002', ' C003 ', 'C004', '', 'c005', None]

# Clean and standardize
clean_ids = [
    cid.strip().upper() 
    for cid in raw_customer_ids 
    if cid and cid.strip()
]
print(f"Raw IDs: {raw_customer_ids}")
print(f"Clean IDs: {clean_ids}\n")

print("="*60 + "\n")

# Performance comparison
import time

# Generate large dataset
large_data = list(range(1000000))

# Traditional loop
start = time.time()
result1 = []
for num in large_data:
    if num % 2 == 0:
        result1.append(num * 2)
traditional_time = time.time() - start

# List comprehension
start = time.time()
result2 = [num * 2 for num in large_data if num % 2 == 0]
comprehension_time = time.time() - start

print("Performance Test (1 million numbers):")
print(f"Traditional Loop: {traditional_time:.4f} seconds")
print(f"List Comprehension: {comprehension_time:.4f} seconds")
print(f"Speedup: {traditional_time/comprehension_time:.2f}x faster! 🚀")