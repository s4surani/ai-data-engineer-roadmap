# tests/test_validators.py - Unit tests for validators module

import sys
sys.path.insert(0, '..')

import pytest
from data_utils import validators


class TestEmailValidation:
    """Test email validation function"""
    
    def test_valid_emails(self):
        """Test valid email addresses"""
        valid_emails = [
            'mayur@example.com',
            'test.user@company.co.in',
            'admin@test-domain.com',
            'user123@example.org'
        ]
        
        for email in valid_emails:
            assert validators.validate_email(email) == True
    
    def test_invalid_emails(self):
        """Test invalid email addresses"""
        invalid_emails = [
            'invalid',
            'missing@domain',
            '@nodomain.com',
            'spaces in@email.com',
            '',
            None
        ]
        
        for email in invalid_emails:
            assert validators.validate_email(email) == False


class TestPhoneValidation:
    """Test phone validation function"""
    
    def test_valid_indian_phones(self):
        """Test valid Indian phone numbers"""
        valid_phones = [
            '9876543210',
            '8765432109',
            '7654321098',
            '6543210987'
        ]
        
        for phone in valid_phones:
            assert validators.validate_phone(phone) == True
    
    def test_invalid_phones(self):
        """Test invalid phone numbers"""
        invalid_phones = [
            '123',
            '12345',
            '1234567890',  # Starts with 1
            '5876543210',  # Starts with 5
            '',
            None
        ]
        
        for phone in invalid_phones:
            assert validators.validate_phone(phone) == False


class TestPriceValidation:
    """Test price validation function"""
    
    def test_valid_prices(self):
        """Test valid prices"""
        assert validators.validate_price(100)[0] == True
        assert validators.validate_price(1000.50)[0] == True
        assert validators.validate_price(0)[0] == True
    
    def test_negative_price(self):
        """Test negative price"""
        is_valid, error = validators.validate_price(-100)
        assert is_valid == False
        assert "negative" in error.lower()
    
    def test_price_range(self):
        """Test price range validation"""
        is_valid, error = validators.validate_price(50, min_price=100)
        assert is_valid == False
        
        is_valid, error = validators.validate_price(1000, max_price=500)
        assert is_valid == False


class TestCustomerIDValidation:
    """Test customer ID validation function"""
    
    def test_valid_customer_ids(self):
        """Test valid customer IDs"""
        valid_ids = ['C001', 'C1234', 'C999999']
        
        for cid in valid_ids:
            is_valid, error = validators.validate_customer_id(cid)
            assert is_valid == True
    
    def test_invalid_customer_ids(self):
        """Test invalid customer IDs"""
        invalid_ids = [
            'INVALID',  # Wrong prefix
            'C',        # Too short
            'C12A',     # Non-numeric suffix
            '',         # Empty
            None        # None
        ]
        
        for cid in invalid_ids:
            is_valid, error = validators.validate_customer_id(cid)
            assert is_valid == False


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, '-v'])