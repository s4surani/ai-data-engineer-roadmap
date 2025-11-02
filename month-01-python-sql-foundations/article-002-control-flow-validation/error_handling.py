# error_handling.py - Mastering Error Handling

import pandas as pd

def safe_divide(a, b):
    """Safely divide two numbers"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print(f"❌ Error: Cannot divide {a} by zero")
        return None
    except TypeError:
        print(f"❌ Error: Invalid types - {type(a)}, {type(b)}")
        return None

# Test safe division
print("Safe Division Tests:")
print(f"10 / 2 = {safe_divide(10, 2)}")
print(f"10 / 0 = {safe_divide(10, 0)}")
print(f"10 / 'abc' = {safe_divide(10, 'abc')}")

print("\n" + "="*60 + "\n")

def load_csv_safe(file_path):
    """Safely load CSV with error handling"""
    try:
        print(f"📂 Attempting to load {file_path}...")
        df = pd.read_csv(file_path)
        print(f"✅ Successfully loaded {len(df)} records")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return None
    except pd.errors.EmptyDataError:
        print(f"❌ Error: File is empty")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
    finally:
        print("🔄 Load attempt completed\n")

# Test file loading
print("File Loading Tests:")
load_csv_safe('test_sales_data.csv')  # Exists
load_csv_safe('nonexistent.csv')      # Doesn't exist

print("="*60 + "\n")

# Multiple exception handling
def process_record(record):
    """Process record with comprehensive error handling"""
    try:
        # Attempt to calculate revenue
        revenue = record['price'] * record['quantity']
        
        # Attempt to format customer ID
        customer_id = record['customer_id'].upper()
        
        print(f"✅ Processed: {customer_id} - ₹{revenue:,}")
        return True
        
    except KeyError as e:
        print(f"❌ Missing field: {e}")
        return False
    except TypeError as e:
        print(f"❌ Type error: {e}")
        return False
    except AttributeError as e:
        print(f"❌ Attribute error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

# Test record processing
print("Record Processing Tests:")
process_record({'price': 1000, 'quantity': 2, 'customer_id': 'c001'})
process_record({'price': 1000, 'quantity': 2})  # Missing customer_id
process_record({'price': 1000, 'quantity': 'abc', 'customer_id': 'c001'})  # Invalid type