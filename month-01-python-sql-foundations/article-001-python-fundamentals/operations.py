# operations.py - Python Operations

# ARITHMETIC OPERATIONS
revenue = 100000
costs = 65000
profit = revenue - costs

print("Financial Calculations:")
print(f"Revenue: ₹{revenue:,}")
print(f"Costs: ₹{costs:,}")
print(f"Profit: ₹{profit:,}")
print(f"Profit Margin: {(profit/revenue)*100:.2f}%")

print("\n" + "="*50 + "\n")

# STRING OPERATIONS
first_name = "Suresh"
last_name = "Surani"
full_name = first_name + " " + last_name  # Concatenation

email = f"{first_name.lower()}.{last_name.lower()}@company.com"
print(f"Full Name: {full_name}")
print(f"Email: {email}")
print(f"Name Length: {len(full_name)} characters")
print(f"Uppercase: {full_name.upper()}")

print("\n" + "="*50 + "\n")

# COMPARISON OPERATIONS
target_sales = 500000
actual_sales = 520000

print("Sales Performance:")
print(f"Target Met: {actual_sales >= target_sales}")
print(f"Exceeded by: ₹{actual_sales - target_sales:,}")

if actual_sales > target_sales:
    bonus_percentage = 10
    print(f"Bonus Earned: {bonus_percentage}%")
else:
    bonus_percentage = 0
    print("No bonus this quarter")

print("\n" + "="*50 + "\n")

# LOGICAL OPERATIONS
has_python_skill = True
has_sql_skill = True
has_aws_skill = False

is_qualified = has_python_skill and has_sql_skill
print(f"Qualified for Data Engineer role: {is_qualified}")

is_cloud_ready = has_python_skill and has_sql_skill and has_aws_skill
print(f"Cloud-ready: {is_cloud_ready}")

print("\n" + "="*50 + "\n")

# LIST OPERATIONS
monthly_sales = [45000, 52000, 48000, 61000, 58000, 63000]

print("Sales Analytics:")
print(f"Total Sales: ₹{sum(monthly_sales):,}")
print(f"Average Sales: ₹{sum(monthly_sales)/len(monthly_sales):,.2f}")
print(f"Highest Month: ₹{max(monthly_sales):,}")
print(f"Lowest Month: ₹{min(monthly_sales):,}")
print(f"Number of Months: {len(monthly_sales)}")