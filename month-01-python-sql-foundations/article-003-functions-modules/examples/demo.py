# examples/demo.py - Demonstration of data_utils package

"""
This script demonstrates how to use the data_utils package
in a real data engineering scenario.
"""

import sys
sys.path.insert(0, '..')  # Add parent directory to path

from data_utils import validators, calculators, formatters
import pandas as pd


def process_sales_record(record):
    """
    Process a single sales record with validation and calculations
    
    Args:
        record (dict): Sales record
        
    Returns:
        dict: Processed record with validation results
    """
    result = {
        'original': record,
        'valid': True,
        'errors': [],
        'calculated': {}
    }
    
    # Validate price
    price_valid, price_error = validators.validate_price(
        record.get('price', 0),
        min_price=0,
        max_price=1000000
    )
    if not price_valid:
        result['valid'] = False
        result['errors'].append(price_error)
    
    # Validate quantity
    qty_valid, qty_error = validators.validate_quantity(
        record.get('quantity', 0)
    )
    if not qty_valid:
        result['valid'] = False
        result['errors'].append(qty_error)
    
    # Validate customer ID
    cust_valid, cust_error = validators.validate_customer_id(
        record.get('customer_id', '')
    )
    if not cust_valid:
        result['valid'] = False
        result['errors'].append(cust_error)
    
    # If valid, calculate metrics
    if result['valid']:
        revenue = calculators.calculate_revenue(
            record['price'],
            record['quantity']
        )
        
        # Apply discount if high value
        if revenue > 100000:
            disc_price, disc_amt = calculators.calculate_discount(
                revenue, 10  # 10% discount
            )
            result['calculated']['discount_applied'] = True
            result['calculated']['discount_amount'] = disc_amt
            result['calculated']['final_revenue'] = disc_price
        else:
            result['calculated']['discount_applied'] = False
            result['calculated']['final_revenue'] = revenue
        
        result['calculated']['revenue'] = revenue
    
    return result


def main():
    """Main demonstration function"""
    print("="*70)
    print("🚀 DATA UTILS PACKAGE DEMONSTRATION")
    print("="*70 + "\n")
    
    # Sample sales data
    sales_data = [
        {
            'product': 'Laptop',
            'price': 75000,
            'quantity': 3,
            'customer_id': 'C001'
        },
        {
            'product': 'Mouse',
            'price': -500,  # Invalid: negative price
            'quantity': 10,
            'customer_id': 'C002'
        },
        {
            'product': 'Monitor',
            'price': 25000,
            'quantity': 5,
            'customer_id': 'INVALID'  # Invalid: wrong format
        },
        {
            'product': 'Keyboard',
            'price': 1500,
            'quantity': 2,
            'customer_id': 'C003'
        }
    ]
    
    print("📊 Processing Sales Records:\n")
    
    valid_count = 0
    invalid_count = 0
    total_revenue = 0
    
    for idx, record in enumerate(sales_data, 1):
        print(f"Record #{idx}: {record['product']}")
        
        result = process_sales_record(record)
        
        if result['valid']:
            print("  ✅ VALID")
            valid_count += 1
            
            revenue = result['calculated']['revenue']
            final_revenue = result['calculated']['final_revenue']
            
            print(f"     Revenue: {formatters.format_currency(revenue)}")
            
            if result['calculated']['discount_applied']:
                discount = result['calculated']['discount_amount']
                print(f"     Discount: {formatters.format_currency(discount)} (10%)")
                print(f"     Final: {formatters.format_currency(final_revenue)}")
            
            total_revenue += final_revenue
        else:
            print("  ❌ INVALID")
            invalid_count += 1
            for error in result['errors']:
                print(f"     - {error}")
        
        print()
    
    # Summary
    print("="*70)
    print("📈 SUMMARY")
    print("="*70)
    print(f"Total Records: {len(sales_data)}")
    print(f"Valid: {valid_count} ({formatters.format_percentage(valid_count/len(sales_data))})")
    print(f"Invalid: {invalid_count} ({formatters.format_percentage(invalid_count/len(sales_data))})")
    print(f"Total Revenue: {formatters.format_currency(total_revenue)}")
    print("="*70 + "\n")
    
    # Demonstrate other utilities
    print("🔧 Additional Utility Demonstrations:\n")
    
    # Email validation
    emails = ['mayur@example.com', 'invalid-email', 'test@company.co.in']
    print("Email Validation:")
    for email in emails:
        is_valid = validators.validate_email(email)
        status = "✅" if is_valid else "❌"
        print(f"  {status} {email}")
    
    print()
    
    # Phone validation
    phones = ['9876543210', '1234567890', '123']
    print("Phone Validation:")
    for phone in phones:
        is_valid = validators.validate_phone(phone)
        status = "✅" if is_valid else "❌"
        formatted = formatters.format_phone(phone) if is_valid else phone
        print(f"  {status} {formatted}")
    
    print()
    
    # Metrics calculation
    monthly_sales = [45000, 52000, 48000, 61000, 58000, 63000]
    metrics = calculators.calculate_metrics(monthly_sales)
    
    print("Monthly Sales Metrics:")
    print(f"  Total: {formatters.format_currency(metrics['total'])}")
    print(f"  Average: {formatters.format_currency(metrics['average'])}")
    print(f"  Highest: {formatters.format_currency(metrics['max'])}")
    print(f"  Lowest: {formatters.format_currency(metrics['min'])}")
    
    print()
    
    # Growth rate
    old_revenue = 500000
    new_revenue = 650000
    growth = calculators.calculate_growth_rate(old_revenue, new_revenue)
    
    print("Revenue Growth:")
    print(f"  Previous: {formatters.format_currency(old_revenue)}")
    print(f"  Current: {formatters.format_currency(new_revenue)}")
    print(f"  Growth: {formatters.format_percentage(growth)}")
    
    print("\n" + "="*70)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()