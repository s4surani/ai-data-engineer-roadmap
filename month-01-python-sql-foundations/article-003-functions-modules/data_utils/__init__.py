# data_utils/__init__.py - Package initialization

"""
Data Utils - A comprehensive data engineering utility library

This package provides utilities for:
- Data validation (validators module)
- Business calculations (calculators module)
- Data formatting (formatters module)

Example usage:
    from data_utils import validators, calculators, formatters
    
    # Validate email
    is_valid = validators.validate_email("user@example.com")
    
    # Calculate revenue
    revenue = calculators.calculate_revenue(1000, 50)
    
    # Format currency
    formatted = formatters.format_currency(revenue)
"""

__version__ = '1.0.0'
__author__ = 'Mayurkumar Surani'
__email__ = 'mayur@example.com'

# Import main modules
from . import validators
from . import calculators
from . import formatters

# Expose commonly used functions at package level
from .validators import (
    validate_email,
    validate_phone,
    validate_price,
    validate_customer_id
)

from .calculators import (
    calculate_revenue,
    calculate_profit,
    calculate_metrics
)

from .formatters import (
    format_currency,
    format_percentage,
    format_number
)

__all__ = [
    # Modules
    'validators',
    'calculators',
    'formatters',
    
    # Functions
    'validate_email',
    'validate_phone',
    'validate_price',
    'validate_customer_id',
    'calculate_revenue',
    'calculate_profit',
    'calculate_metrics',
    'format_currency',
    'format_percentage',
    'format_number',
]