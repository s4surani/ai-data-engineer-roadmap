# validators.py - Data Validation Utilities

"""
Data validation utilities for data engineering pipelines.

This module provides functions to validate common data types
and business rules in data processing workflows.
"""

import re
from datetime import datetime
import pandas as pd


def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Examples:
        >>> validate_email("mayur@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone, country_code='IN'):
    """
    Validate phone number
    
    Args:
        phone (str): Phone number to validate
        country_code (str): Country code (default: 'IN')
        
    Returns:
        bool: True if valid, False otherwise
        
    Examples:
        >>> validate_phone("9876543210")
        True
        >>> validate_phone("123")
        False
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove spaces and dashes
    phone = phone.replace(' ', '').replace('-', '')
    
    if country_code == 'IN':
        # Indian mobile: 10 digits starting with 6-9
        pattern = r'^[6-9]\d{9}$'
        return bool(re.match(pattern, phone))
    
    return False


def validate_price(price, min_price=0, max_price=float('inf')):
    """
    Validate price value
    
    Args:
        price (float): Price to validate
        min_price (float): Minimum allowed price
        max_price (float): Maximum allowed price
        
    Returns:
        tuple: (is_valid, error_message)
        
    Examples:
        >>> validate_price(1000)
        (True, None)
        >>> validate_price(-100)
        (False, 'Price cannot be negative')
    """
    try:
        price = float(price)
    except (ValueError, TypeError):
        return False, "Invalid price format"
    
    if price < 0:
        return False, "Price cannot be negative"
    
    if price < min_price:
        return False, f"Price below minimum: ₹{min_price}"
    
    if price > max_price:
        return False, f"Price above maximum: ₹{max_price}"
    
    return True, None


def validate_quantity(quantity, min_qty=1, max_qty=10000):
    """
    Validate quantity value
    
    Args:
        quantity (int): Quantity to validate
        min_qty (int): Minimum allowed quantity
        max_qty (int): Maximum allowed quantity
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return False, "Invalid quantity format"
    
    if quantity < min_qty:
        return False, f"Quantity below minimum: {min_qty}"
    
    if quantity > max_qty:
        return False, f"Quantity above maximum: {max_qty}"
    
    return True, None


def validate_date(date_str, date_format='%Y-%m-%d'):
    """
    Validate date string
    
    Args:
        date_str (str): Date string to validate
        date_format (str): Expected date format
        
    Returns:
        tuple: (is_valid, parsed_date or error_message)
        
    Examples:
        >>> validate_date("2025-01-15")
        (True, datetime.datetime(2025, 1, 15, 0, 0))
    """
    try:
        parsed_date = datetime.strptime(date_str, date_format)
        return True, parsed_date
    except (ValueError, TypeError):
        return False, f"Invalid date format. Expected: {date_format}"


def validate_customer_id(customer_id, prefix='C', min_length=4):
    """
    Validate customer ID format
    
    Args:
        customer_id (str): Customer ID to validate
        prefix (str): Expected prefix
        min_length (int): Minimum length
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not customer_id or not isinstance(customer_id, str):
        return False, "Customer ID is required"
    
    customer_id = customer_id.strip().upper()
    
    if not customer_id.startswith(prefix):
        return False, f"Customer ID must start with '{prefix}'"
    
    if len(customer_id) < min_length:
        return False, f"Customer ID too short (min: {min_length})"
    
    # Check if remaining part is numeric
    id_number = customer_id[len(prefix):]
    if not id_number.isdigit():
        return False, "Customer ID must end with numbers"
    
    return True, None


def validate_region(region, valid_regions=None):
    """
    Validate region value
    
    Args:
        region (str): Region to validate
        valid_regions (list): List of valid regions
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if valid_regions is None:
        valid_regions = ['North', 'South', 'East', 'West']
    
    if not region or not isinstance(region, str):
        return False, "Region is required"
    
    if region not in valid_regions:
        return False, f"Invalid region. Must be one of: {', '.join(valid_regions)}"
    
    return True, None


def validate_dataframe_schema(df, required_columns):
    """
    Validate DataFrame has required columns
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        required_columns (list): List of required column names
        
    Returns:
        tuple: (is_valid, missing_columns)
    """
    if not isinstance(df, pd.DataFrame):
        return False, ["Input is not a DataFrame"]
    
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        return False, missing
    
    return True, []


# Module-level constants
DEFAULT_REGIONS = ['North', 'South', 'East', 'West']
DEFAULT_CUSTOMER_PREFIX = 'C'
DEFAULT_MIN_PRICE = 0
DEFAULT_MAX_PRICE = 10000000

if __name__ == "__main__":
    # Test the validators
    print("Testing validators module...\n")
    
    print("Email validation:")
    print(f"  mayur@example.com: {validate_email('mayur@example.com')}")
    print(f"  invalid: {validate_email('invalid')}")
    
    print("\nPhone validation:")
    print(f"  9876543210: {validate_phone('9876543210')}")
    print(f"  123: {validate_phone('123')}")
    
    print("\nPrice validation:")
    print(f"  1000: {validate_price(1000)}")
    print(f"  -100: {validate_price(-100)}")
    
    print("\nCustomer ID validation:")
    print(f"  C001: {validate_customer_id('C001')}")
    print(f"  INVALID: {validate_customer_id('INVALID')}")