# loops_basics.py - Understanding For Loops

# Loop through a list
products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones']

print("Product Catalog:")
for product in products:
    print(f"  - {product}")

print("\n" + "="*60 + "\n")

# Loop with index using enumerate
print("Product Catalog (with index):")
for index, product in enumerate(products, start=1):
    print(f"  {index}. {product}")

print("\n" + "="*60 + "\n")

# Loop through a range
print("Processing batches:")
for batch_number in range(1, 6):
    print(f"  Processing batch {batch_number}...")
    # Simulate processing
    records_processed = batch_number * 100
    print(f"  ✅ {records_processed} records processed")

print("\n" + "="*60 + "\n")

# Loop through dictionary
employee = {
    'name': 'Surani',
    'role': 'Data Engineer',
    'experience': 3,
    'location': 'Pune'
}

print("Employee Details:")
for key, value in employee.items():
    print(f"  {key.capitalize()}: {value}")

print("\n" + "="*60 + "\n")

# Nested loops (loop within loop)
regions = ['North', 'South', 'East', 'West']
products = ['Laptop', 'Mouse']

print("Sales Matrix:")
for region in regions:
    for product in products:
        print(f"  {region} - {product}: Processing...")

print("\n" + "="*60 + "\n")

# Loop with conditional (filtering)
sales_data = [45000, 52000, 38000, 61000, 48000, 72000]

print("High-performing months (>50k):")
for month, sales in enumerate(sales_data, start=1):
    if sales > 50000:
        print(f"  Month {month}: ₹{sales:,} ⭐")