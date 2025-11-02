# formatters.py - Data Formatting Utilities

"""
Data formatting utilities for data engineering pipelines.

This module provides functions to format data for display,
export, and reporting purposes.
"""

from datetime import datetime
from typing import Any, List, Dict


def format_currency(amount, currency='₹', decimals=2):
    """
    Format amount as currency
    
    Args:
        amount (float): Amount to format
        currency (str): Currency symbol
        decimals (int): Decimal places
        
    Returns:
        str: Formatted currency string
    """
    return f"{currency}{amount:,.{decimals}f}"


def format_percentage(value, decimals=1):
    """
    Format value as percentage
    
    Args:
        value (float): Value to format (0-1 or 0-100)
        decimals (int): Decimal places
        
    Returns:
        str: Formatted percentage string
    """
    # If value is between 0-1, convert to percentage
    if 0 <= value <= 1:
        value = value * 100
    
    return f"{value:.{decimals}f}%"


def format_number(number, decimals=0):
    """
    Format number with thousand separators
    
    Args:
        number (float): Number to format
        decimals (int): Decimal places
        
    Returns:
        str: Formatted number string
    """
    return f"{number:,.{decimals}f}"


def format_date(date, format_str='%Y-%m-%d'):
    """
    Format date object as string
    
    Args:
        date (datetime): Date to format
        format_str (str): Format string
        
    Returns:
        str: Formatted date string
    """
    if isinstance(date, str):
        return date
    
    return date.strftime(format_str)


def format_phone(phone, country_code='IN'):
    """
    Format phone number
    
    Args:
        phone (str): Phone number
        country_code (str): Country code
        
    Returns:
        str: Formatted phone number
    """
    # Remove all non-digits
    digits = ''.join(filter(str.isdigit, phone))
    
    if country_code == 'IN' and len(digits) == 10:
        return f"+91 {digits[:5]} {digits[5:]}"
    
    return phone


def format_file_size(size_bytes):
    """
    Format file size in human-readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} PB"


def format_duration(seconds):
    """
    Format duration in human-readable format
    
    Args:
        seconds (float): Duration in seconds
        
    Returns:
        str: Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.2f} hours"


def format_table(data: List[Dict], headers: List[str] = None):
    """
    Format data as ASCII table
    
    Args:
        data (list): List of dictionaries
        headers (list): Column headers (optional)
        
    Returns:
        str: Formatted table string
    """
    if not data:
        return "No data to display"
    
    if headers is None:
        headers = list(data[0].keys())
    
    # Calculate column widths
    col_widths = {h: len(str(h)) for h in headers}
    for row in data:
        for header in headers:
            value = str(row.get(header, ''))
            col_widths[header] = max(col_widths[header], len(value))
    
    # Build table
    lines = []
    
    # Header
    header_line = " | ".join(
        str(h).ljust(col_widths[h]) for h in headers
    )
    lines.append(header_line)
    lines.append("-" * len(header_line))
    
    # Rows
    for row in data:
        row_line = " | ".join(
            str(row.get(h, '')).ljust(col_widths[h]) for h in headers
        )
        lines.append(row_line)
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test the formatters
    print("Testing formatters module...\n")
    
    print("Currency formatting:")
    print(f"  {format_currency(1234567.89)}")
    print(f"  {format_currency(999.5, currency='$')}")
    
    print("\nPercentage formatting:")
    print(f"  {format_percentage(0.156)}")
    print(f"  {format_percentage(85.7)}")
    
    print("\nNumber formatting:")
    print(f"  {format_number(1234567)}")
    print(f"  {format_number(1234.5678, decimals=2)}")
    
    print("\nFile size formatting:")
    print(f"  {format_file_size(1024)}")
    print(f"  {format_file_size(1048576)}")
    print(f"  {format_file_size(1073741824)}")
    
    print("\nTable formatting:")
    data = [
        {'name': 'Mayurkumar', 'role': 'Data Engineer', 'exp': 3},
        {'name': 'Rahul', 'role': 'Senior DE', 'exp': 5},
        {'name': 'Priya', 'role': 'Lead DE', 'exp': 8}
    ]
    print(format_table(data))