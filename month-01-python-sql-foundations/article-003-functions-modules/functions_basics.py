# functions_basics.py - Understanding Functions

# Simple function (no parameters, no return)
def greet():
    """Print a greeting message"""
    print("Hello, Data Engineer! 👋")

greet()

print("\n" + "="*60 + "\n")

# Function with parameters
def greet_person(name):
    """
    Greet a person by name
    
    Args:
        name (str): Person's name
    """
    print(f"Hello, {name}! Welcome to Data Engineering! 🚀")

greet_person("Mayurkumar")
greet_person("Surani")

print("\n" + "="*60 + "\n")

# Function with return value
def calculate_revenue(price, quantity):
    """
    Calculate total revenue
    
    Args:
        price (float): Unit price
        quantity (int): Quantity sold
        
    Returns:
        float: Total revenue
    """
    revenue = price * quantity
    return revenue

laptop_revenue = calculate_revenue(75000, 5)
print(f"Laptop Revenue: ₹{laptop_revenue:,}")

mouse_revenue = calculate_revenue(500, 100)
print(f"Mouse Revenue: ₹{mouse_revenue:,}")

print("\n" + "="*60 + "\n")

# Function with multiple return values
def calculate_metrics(sales_data):
    """
    Calculate sales metrics
    
    Args:
        sales_data (list): List of sales amounts
        
    Returns:
        tuple: (total, average, max, min)
    """
    total = sum(sales_data)
    average = total / len(sales_data)
    maximum = max(sales_data)
    minimum = min(sales_data)
    
    return total, average, maximum, minimum

sales = [45000, 52000, 48000, 61000, 58000]
total, avg, max_sale, min_sale = calculate_metrics(sales)

print("Sales Metrics:")
print(f"  Total: ₹{total:,}")
print(f"  Average: ₹{avg:,.2f}")
print(f"  Highest: ₹{max_sale:,}")
print(f"  Lowest: ₹{min_sale:,}")

print("\n" + "="*60 + "\n")

# Function with default parameters
def create_employee_record(name, role, experience=0, location="Pune"):
    """
    Create employee record with defaults
    
    Args:
        name (str): Employee name
        role (str): Job role
        experience (int): Years of experience (default: 0)
        location (str): Work location (default: "Pune")
        
    Returns:
        dict: Employee record
    """
    return {
        'name': name,
        'role': role,
        'experience': experience,
        'location': location
    }

# Using defaults
emp1 = create_employee_record("Mayurkumar Surani", "Data Engineer")
print("Employee 1:", emp1)

# Overriding defaults
emp2 = create_employee_record("Rahul Sharma", "Senior Data Engineer", 
                              experience=5, location="Mumbai")
print("Employee 2:", emp2)

print("\n" + "="*60 + "\n")

# Function with keyword arguments
def generate_report(title, data, format="PDF", include_charts=True, 
                   color_scheme="blue"):
    """
    Generate a report with flexible options
    
    Args:
        title (str): Report title
        data (dict): Report data
        format (str): Output format
        include_charts (bool): Include visualizations
        color_scheme (str): Color theme
    """
    print(f"📊 Generating Report: {title}")
    print(f"   Format: {format}")
    print(f"   Charts: {'Yes' if include_charts else 'No'}")
    print(f"   Theme: {color_scheme}")
    print(f"   Data points: {len(data)}")

# Call with keyword arguments (order doesn't matter!)
generate_report(
    title="Q4 Sales Report",
    data={'jan': 100, 'feb': 120, 'mar': 110},
    color_scheme="green",
    format="Excel"
)

print("\n" + "="*60 + "\n")

# Function with *args (variable positional arguments)
def calculate_total_sales(*sales):
    """
    Calculate total from any number of sales values
    
    Args:
        *sales: Variable number of sales amounts
        
    Returns:
        float: Total sales
    """
    total = sum(sales)
    print(f"Calculating total from {len(sales)} values...")
    return total

# Can pass any number of arguments
total1 = calculate_total_sales(1000, 2000, 3000)
print(f"Total 1: ₹{total1:,}")

total2 = calculate_total_sales(5000, 10000, 15000, 20000, 25000)
print(f"Total 2: ₹{total2:,}")

print("\n" + "="*60 + "\n")

# Function with **kwargs (variable keyword arguments)
def create_product(**attributes):
    """
    Create product with flexible attributes
    
    Args:
        **attributes: Variable keyword arguments
        
    Returns:
        dict: Product dictionary
    """
    print(f"Creating product with {len(attributes)} attributes:")
    for key, value in attributes.items():
        print(f"  {key}: {value}")
    return attributes

product1 = create_product(
    name="Laptop",
    price=75000,
    brand="Dell",
    warranty="3 years"
)

print()

product2 = create_product(
    name="Mouse",
    price=500,
    brand="Logitech",
    wireless=True,
    color="Black"
)