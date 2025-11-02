# conditionals_basics.py - Understanding Conditionals

# Simple if statement
sales_amount = 150000
target = 100000

if sales_amount > target:
    print(f"🎉 Target achieved! Sales: ₹{sales_amount:,}")
    bonus = sales_amount * 0.10
    print(f"💰 Bonus earned: ₹{bonus:,}")

print("\n" + "="*60 + "\n")

# if-else statement
inventory_count = 5
reorder_level = 10

if inventory_count < reorder_level:
    print(f"⚠️  Low inventory: {inventory_count} units")
    print("📦 Reorder required!")
else:
    print(f"✅ Inventory sufficient: {inventory_count} units")

print("\n" + "="*60 + "\n")

# if-elif-else (multiple conditions)
customer_type = "premium"
order_value = 50000

if customer_type == "premium":
    discount = 0.20
    print(f"💎 Premium customer - 20% discount")
elif customer_type == "gold":
    discount = 0.15
    print(f"🥇 Gold customer - 15% discount")
elif customer_type == "silver":
    discount = 0.10
    print(f"🥈 Silver customer - 10% discount")
else:
    discount = 0.05
    print(f"👤 Regular customer - 5% discount")

final_amount = order_value * (1 - discount)
print(f"Order Value: ₹{order_value:,}")
print(f"Final Amount: ₹{final_amount:,}")

print("\n" + "="*60 + "\n")

# Nested conditionals
age = 28
experience_years = 3
has_certification = True

print("Job Application Evaluation:")

if age >= 21:
    if experience_years >= 2:
        if has_certification:
            print("✅ APPROVED - All criteria met")
            print("   - Age: Qualified")
            print("   - Experience: Sufficient")
            print("   - Certification: Valid")
        else:
            print("⚠️  CONDITIONAL - Certification missing")
    else:
        print("❌ REJECTED - Insufficient experience")
else:
    print("❌ REJECTED - Age requirement not met")

print("\n" + "="*60 + "\n")

# Logical operators (and, or, not)
revenue = 500000
profit_margin = 0.25
customer_satisfaction = 4.5

is_healthy_business = (
    revenue > 400000 and 
    profit_margin > 0.20 and 
    customer_satisfaction >= 4.0
)

print("Business Health Check:")
print(f"Revenue: ₹{revenue:,}")
print(f"Profit Margin: {profit_margin*100}%")
print(f"Customer Satisfaction: {customer_satisfaction}/5")
print(f"\nBusiness Status: {'✅ HEALTHY' if is_healthy_business else '⚠️  NEEDS ATTENTION'}")