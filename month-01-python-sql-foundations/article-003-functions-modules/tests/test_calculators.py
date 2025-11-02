# tests/test_calculators.py - Unit tests for calculators module

import sys
sys.path.insert(0, '..')

import pytest
from data_utils import calculators


class TestRevenueCalculation:
    """Test revenue calculation function"""
    
    def test_basic_revenue(self):
        """Test basic revenue calculation"""
        assert calculators.calculate_revenue(100, 10) == 1000
        assert calculators.calculate_revenue(50.5, 20) == 1010
    
    def test_zero_values(self):
        """Test with zero values"""
        assert calculators.calculate_revenue(0, 10) == 0
        assert calculators.calculate_revenue(100, 0) == 0


class TestProfitCalculation:
    """Test profit calculation functions"""
    
    def test_basic_profit(self):
        """Test basic profit calculation"""
        assert calculators.calculate_profit(1000, 600) == 400
        assert calculators.calculate_profit(500, 300) == 200
    
    def test_profit_margin(self):
        """Test profit margin calculation"""
        margin = calculators.calculate_profit_margin(1000, 600)
        assert margin == 0.4  # 40%
        
        margin = calculators.calculate_profit_margin(500, 400)
        assert margin == 0.2  # 20%
    
    def test_zero_revenue(self):
        """Test profit margin with zero revenue"""
        margin = calculators.calculate_profit_margin(0, 100)
        assert margin == 0.0


class TestDiscountCalculation:
    """Test discount calculation function"""
    
    def test_basic_discount(self):
        """Test basic discount calculation"""
        disc_price, disc_amt = calculators.calculate_discount(1000, 10)
        assert disc_price == 900
        assert disc_amt == 100
    
    def test_various_discounts(self):
        """Test various discount percentages"""
        disc_price, disc_amt = calculators.calculate_discount(500, 20)
        assert disc_price == 400
        assert disc_amt == 100
        
        disc_price, disc_amt = calculators.calculate_discount(1000, 50)
        assert disc_price == 500
        assert disc_amt == 500


class TestMetricsCalculation:
    """Test metrics calculation function"""
    
    def test_basic_metrics(self):
        """Test basic metrics calculation"""
        data = [10, 20, 30, 40, 50]
        metrics = calculators.calculate_metrics(data)
        
        assert metrics['total'] == 150
        assert metrics['average'] == 30
        assert metrics['min'] == 10
        assert metrics['max'] == 50
        assert metrics['count'] == 5
    
    def test_empty_data(self):
        """Test with empty data"""
        metrics = calculators.calculate_metrics([])
        assert metrics['total'] == 0
        assert metrics['count'] == 0


class TestGrowthRate:
    """Test growth rate calculation"""
    
    def test_positive_growth(self):
        """Test positive growth"""
        growth = calculators.calculate_growth_rate(100, 150)
        assert growth == 50.0  # 50% growth
    
    def test_negative_growth(self):
        """Test negative growth"""
        growth = calculators.calculate_growth_rate(100, 80)
        assert growth == -20.0  # -20% decline
    
    def test_zero_growth(self):
        """Test zero growth"""
        growth = calculators.calculate_growth_rate(100, 100)
        assert growth == 0.0


if __name__ == "__main__":
    pytest.main([__file__, '-v'])