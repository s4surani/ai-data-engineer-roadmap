# calculators.py - Business Calculation Utilities

"""
Business calculation utilities for data engineering pipelines.

This module provides functions for common business calculations
like revenue, profit, discounts, and metrics.
"""

from typing import List, Dict, Tuple
import pandas as pd


def calculate_revenue(price, quantity):
    """
    Calculate revenue from price and quantity
    
    Args:
        price (float): Unit price
        quantity (int): Quantity sold
        
    Returns:
        float: Total revenue
    """
    return float(price) * int(quantity)


def calculate_profit(revenue, cost):
    """
    Calculate profit
    
    Args:
        revenue (float): Total revenue
        cost (float): Total cost
        
    Returns:
        float: Profit amount
    """
    return float(revenue) - float(cost)


def calculate_profit_margin(revenue, cost):
    """
    Calculate profit margin percentage
    
    Args:
        revenue (float): Total revenue
        cost (float): Total cost
        
    Returns:
        float: Profit margin (0-1)
    """
    if revenue == 0:
        return 0.0
    
    profit = calculate_profit(revenue, cost)
    return profit / revenue


def calculate_discount(original_price, discount_percentage):
    """
    Calculate discounted price
    
    Args:
        original_price (float): Original price
        discount_percentage (float): Discount percentage (0-100)
        
    Returns:
        tuple: (discounted_price, discount_amount)
    """
    discount_amount = original_price * (discount_percentage / 100)
    discounted_price = original_price - discount_amount
    
    return discounted_price, discount_amount


def calculate_tax(amount, tax_rate):
    """
    Calculate tax amount
    
    Args:
        amount (float): Base amount
        tax_rate (float): Tax rate (0-1)
        
    Returns:
        tuple: (total_with_tax, tax_amount)
    """
    tax_amount = amount * tax_rate
    total_with_tax = amount + tax_amount
    
    return total_with_tax, tax_amount


def calculate_average(values: List[float]) -> float:
    """
    Calculate average of values
    
    Args:
        values (list): List of numeric values
        
    Returns:
        float: Average value
    """
    if not values:
        return 0.0
    
    return sum(values) / len(values)


def calculate_growth_rate(old_value, new_value):
    """
    Calculate growth rate percentage
    
    Args:
        old_value (float): Previous value
        new_value (float): Current value
        
    Returns:
        float: Growth rate percentage
    """
    if old_value == 0:
        return 0.0 if new_value == 0 else float('inf')
    
    return ((new_value - old_value) / old_value) * 100


def calculate_metrics(data: List[float]) -> Dict[str, float]:
    """
    Calculate comprehensive metrics for a dataset
    
    Args:
        data (list): List of numeric values
        
    Returns:
        dict: Dictionary of metrics
    """
    if not data:
        return {
            'total': 0,
            'average': 0,
            'min': 0,
            'max': 0,
            'count': 0
        }
    
    return {
        'total': sum(data),
        'average': sum(data) / len(data),
        'min': min(data),
        'max': max(data),
        'count': len(data)
    }


def calculate_roi(investment, returns):
    """
    Calculate Return on Investment
    
    Args:
        investment (float): Initial investment
        returns (float): Total returns
        
    Returns:
        float: ROI percentage
    """
    if investment == 0:
        return 0.0
    
    return ((returns - investment) / investment) * 100


def calculate_moving_average(data: List[float], window: int) -> List[float]:
    """
    Calculate moving average
    
    Args:
        data (list): List of numeric values
        window (int): Window size
        
    Returns:
        list: Moving averages
    """
    if len(data) < window:
        return []
    
    moving_avgs = []
    for i in range(len(data) - window + 1):
        window_data = data[i:i + window]
        moving_avgs.append(sum(window_data) / window)
    
    return moving_avgs


if __name__ == "__main__":
    # Test the calculators
    print("Testing calculators module...\n")
    
    print("Revenue calculation:")
    rev = calculate_revenue(1000, 50)
    print(f"  Price: ₹1000, Quantity: 50 → Revenue: ₹{rev:,}")
    
    print("\nProfit calculation:")
    profit = calculate_profit(50000, 30000)
    margin = calculate_profit_margin(50000, 30000)
    print(f"  Revenue: ₹50000, Cost: ₹30000")
    print(f"  Profit: ₹{profit:,}")
    print(f"  Margin: {margin*100:.1f}%")
    
    print("\nDiscount calculation:")
    disc_price, disc_amt = calculate_discount(1000, 20)
    print(f"  Original: ₹1000, Discount: 20%")
    print(f"  Final Price: ₹{disc_price:.2f}")
    print(f"  Saved: ₹{disc_amt:.2f}")
    
    print("\nMetrics calculation:")
    sales = [45000, 52000, 48000, 61000, 58000]
    metrics = calculate_metrics(sales)
    print(f"  Sales data: {sales}")
    print(f"  Metrics: {metrics}")