# data_validator_v1.py - Basic Data Validation

import pandas as pd

def validate_sales_record(record):
    """
    Validate a single sales record
    
    Args:
        record (dict): Sales record to validate
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    errors = []
    
    # Check if price is positive
    if record['price'] <= 0:
        errors.append(f"Invalid price: {record['price']}")
    
    # Check if quantity is positive
    if record['quantity'] <= 0:
        errors.append(f"Invalid quantity: {record['quantity']}")
    
    # Check if customer_id exists
    if not record['customer_id'] or record['customer_id'].strip() == "":
        errors.append("Missing customer_id")
    
    # Check if product name exists
    if not record['product'] or len(record['product']) < 2:
        errors.append("Invalid product name")
    
    # Check if region is valid
    valid_regions = ['North', 'South', 'East', 'West']
    if record['region'] not in valid_regions:
        errors.append(f"Invalid region: {record['region']}")
    
    # Calculate revenue
    revenue = record['price'] * record['quantity']
    
    # Flag suspiciously high orders
    if revenue > 1000000:
        errors.append(f"⚠️  High value order: ₹{revenue:,} - Needs approval")
    
    is_valid = len(errors) == 0
    return is_valid, errors

# Test data
test_records = [
    {
        'product': 'Laptop',
        'price': 75000,
        'quantity': 2,
        'customer_id': 'C001',
        'region': 'West'
    },
    {
        'product': 'Mouse',
        'price': -500,  # Invalid: negative price
        'quantity': 5,
        'customer_id': 'C002',
        'region': 'East'
    },
    {
        'product': '',  # Invalid: empty product
        'price': 1500,
        'quantity': 0,  # Invalid: zero quantity
        'customer_id': 'C003',
        'region': 'North'
    },
    {
        'product': 'Server',
        'price': 500000,
        'quantity': 3,  # High value order
        'customer_id': 'C004',
        'region': 'South'
    }
]

print("="*60)
print("🔍 DATA VALIDATION REPORT")
print("="*60 + "\n")

valid_count = 0
invalid_count = 0

for idx, record in enumerate(test_records, 1):
    print(f"Record #{idx}: {record['product'] or 'UNNAMED'}")
    is_valid, errors = validate_sales_record(record)
    
    if is_valid:
        print("  ✅ VALID")
        valid_count += 1
    else:
        print("  ❌ INVALID")
        for error in errors:
            print(f"     - {error}")
        invalid_count += 1
    print()

print("="*60)
print(f"Summary: {valid_count} valid, {invalid_count} invalid")
print("="*60)
print("="*60)