# lambda_functions.py - Understanding Lambda Functions

# Regular function
def square(x):
    return x ** 2

print("Regular function:")
print(f"square(5) = {square(5)}")

print("\n" + "="*60 + "\n")

# Lambda equivalent (one-liner)
square_lambda = lambda x: x ** 2

print("Lambda function:")
print(f"square_lambda(5) = {square_lambda(5)}")

print("\n" + "="*60 + "\n")

# Lambda with multiple parameters
calculate_revenue = lambda price, quantity: price * quantity

print("Revenue calculation:")
print(f"Revenue: ₹{calculate_revenue(1000, 50):,}")

print("\n" + "="*60 + "\n")

# Using lambda with map() - apply function to all items
prices = [100, 200, 300, 400, 500]

# Apply 10% discount to all prices
discounted = list(map(lambda price: price * 0.9, prices))

print("Original prices:", prices)
print("Discounted prices:", discounted)

print("\n" + "="*60 + "\n")

# Using lambda with filter() - keep items that match condition
sales_data = [45000, 52000, 38000, 61000, 48000, 72000, 35000]

# Filter high-performing months (>50k)
high_sales = list(filter(lambda sale: sale > 50000, sales_data))

print("All sales:", sales_data)
print("High sales (>50k):", high_sales)

print("\n" + "="*60 + "\n")

# Using lambda with sorted() - custom sorting
employees = [
    {'name': 'Mayurkumar', 'salary': 1200000},
    {'name': 'Rahul', 'salary': 900000},
    {'name': 'Priya', 'salary': 1500000},
    {'name': 'Amit', 'salary': 800000}
]

# Sort by salary (descending)
sorted_employees = sorted(employees, 
                         key=lambda emp: emp['salary'], 
                         reverse=True)

print("Employees sorted by salary:")
for emp in sorted_employees:
    print(f"  {emp['name']}: ₹{emp['salary']:,}")

print("\n" + "="*60 + "\n")

# Real-world example: Data transformation pipeline
raw_data = [
    {'product': 'laptop', 'price': 75000, 'quantity': 2},
    {'product': 'mouse', 'price': 500, 'quantity': 10},
    {'product': 'keyboard', 'price': 1500, 'quantity': 5}
]

# Transform: add revenue, capitalize product names
transformed = list(map(
    lambda item: {
        **item,
        'product': item['product'].upper(),
        'revenue': item['price'] * item['quantity']
    },
    raw_data
))

print("Transformed data:")
for item in transformed:
    print(f"  {item['product']}: ₹{item['revenue']:,}")

print("\n" + "="*60 + "\n")

# Lambda in pandas (data engineering use case)
import pandas as pd

df = pd.DataFrame({
    'product': ['Laptop', 'Mouse', 'Keyboard'],
    'price': [75000, 500, 1500],
    'quantity': [2, 10, 5]
})

# Add revenue column using lambda
df['revenue'] = df.apply(lambda row: row['price'] * row['quantity'], axis=1)

# Add discount column (10% if revenue > 10000)
df['discount'] = df['revenue'].apply(
    lambda rev: 0.10 if rev > 10000 else 0.05
)

print("DataFrame with lambda transformations:")
print(df)