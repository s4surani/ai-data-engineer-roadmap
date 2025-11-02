# csv_operations.py - CSV File Operations

import pandas as pd
import csv
from datetime import datetime
import os


def read_csv_pandas(file_path):
    """
    Read CSV using pandas (recommended for data engineering)
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    try:
        print(f"📂 Reading CSV: {file_path}")
        
        # Basic read
        df = pd.read_csv(file_path)
        
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"   Columns: {', '.join(df.columns)}")
        print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return None
    except pd.errors.EmptyDataError:
        print(f"❌ Error: File is empty")
        return None
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return None


def read_csv_advanced(file_path, **kwargs):
    """
    Read CSV with advanced options
    
    Args:
        file_path (str): Path to CSV file
        **kwargs: Additional pandas read_csv parameters
        
    Returns:
        pd.DataFrame: Loaded data
    """
    try:
        print(f"📂 Reading CSV with advanced options: {file_path}")
        
        # Advanced options
        df = pd.read_csv(
            file_path,
            encoding=kwargs.get('encoding', 'utf-8'),
            sep=kwargs.get('sep', ','),
            header=kwargs.get('header', 0),
            usecols=kwargs.get('usecols', None),
            dtype=kwargs.get('dtype', None),
            parse_dates=kwargs.get('parse_dates', None),
            na_values=kwargs.get('na_values', ['', 'NA', 'NULL']),
            low_memory=False
        )
        
        print(f"✅ Loaded {len(df)} rows")
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def write_csv_pandas(df, file_path, **kwargs):
    """
    Write DataFrame to CSV
    
    Args:
        df (pd.DataFrame): Data to write
        file_path (str): Output file path
        **kwargs: Additional to_csv parameters
    """
    try:
        print(f"💾 Writing CSV: {file_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        df.to_csv(
            file_path,
            index=kwargs.get('index', False),
            encoding=kwargs.get('encoding', 'utf-8'),
            sep=kwargs.get('sep', ',')
        )
        
        file_size = os.path.getsize(file_path) / 1024
        print(f"✅ Saved {len(df)} rows ({file_size:.2f} KB)\n")
        
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")


def read_csv_chunks(file_path, chunk_size=10000):
    """
    Read large CSV in chunks (memory efficient)
    
    Args:
        file_path (str): Path to CSV file
        chunk_size (int): Rows per chunk
        
    Yields:
        pd.DataFrame: Data chunks
    """
    try:
        print(f"📂 Reading CSV in chunks: {file_path}")
        print(f"   Chunk size: {chunk_size:,} rows\n")
        
        chunk_num = 0
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            chunk_num += 1
            print(f"   Processing chunk {chunk_num}: {len(chunk)} rows")
            yield chunk
            
    except Exception as e:
        print(f"❌ Error reading chunks: {e}")


def csv_to_dict(file_path):
    """
    Read CSV as list of dictionaries (using csv module)
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        list: List of dictionaries
    """
    try:
        print(f"📂 Reading CSV as dictionaries: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        print(f"✅ Loaded {len(data)} records\n")
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


# Create sample data
def create_sample_csv():
    """Create sample CSV files for testing"""
    
    # Sample 1: Sales data
    sales_data = {
        'date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05'],
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
        'category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
        'price': [75000, 500, 1500, 25000, 2000],
        'quantity': [2, 10, 5, 1, 4],
        'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'region': ['West', 'East', 'North', 'South', 'West']
    }
    
    df = pd.DataFrame(sales_data)
    df.to_csv('sample_sales.csv', index=False)
    print("✅ Created: sample_sales.csv")
    
    # Sample 2: Large dataset (for chunk reading)
    large_data = {
        'id': range(1, 50001),
        'value': [i * 10 for i in range(1, 50001)],
        'category': ['A' if i % 2 == 0 else 'B' for i in range(1, 50001)]
    }
    
    df_large = pd.DataFrame(large_data)
    df_large.to_csv('large_dataset.csv', index=False)
    print("✅ Created: large_dataset.csv (50,000 rows)")
    
    # Sample 3: CSV with encoding issues
    special_data = {
        'name': ['Mayurkumar', 'Priya', 'Rahul', 'Amit'],
        'city': ['Pune', 'Mumbai', 'Bangalore', 'Delhi'],
        'comment': ['Great product! 👍', 'Excellent service ⭐', 'Fast delivery 🚀', 'Good quality ✅']
    }
    
    df_special = pd.DataFrame(special_data)
    df_special.to_csv('special_chars.csv', index=False, encoding='utf-8')
    print("✅ Created: special_chars.csv (with emojis)\n")


if __name__ == "__main__":
    print("="*70)
    print("📊 CSV OPERATIONS DEMONSTRATION")
    print("="*70 + "\n")
    
    # Create sample files
    create_sample_csv()
    
    # Basic read
    print("1. Basic CSV Read:")
    df = read_csv_pandas('sample_sales.csv')
    if df is not None:
        print(df.head())
    print()
    
    # Advanced read with options
    print("2. Advanced CSV Read (specific columns):")
    df_subset = read_csv_advanced(
        'sample_sales.csv',
        usecols=['product', 'price', 'quantity'],
        dtype={'price': float, 'quantity': int}
    )
    if df_subset is not None:
        print(df_subset.head())
    print()
    
    # Write CSV
    print("3. Write CSV:")
    if df is not None:
        # Add calculated column
        df['revenue'] = df['price'] * df['quantity']
        write_csv_pandas(df, 'output/sales_with_revenue.csv')
    
    # Read in chunks
    print("4. Read Large CSV in Chunks:")
    total_sum = 0
    chunk_count = 0
    for chunk in read_csv_chunks('large_dataset.csv', chunk_size=10000):
        total_sum += chunk['value'].sum()
        chunk_count += 1
    print(f"\n   Total chunks processed: {chunk_count}")
    print(f"   Sum of all values: {total_sum:,}\n")
    
    # Read as dictionaries
    print("5. Read CSV as Dictionaries:")
    records = csv_to_dict('sample_sales.csv')
    if records:
        print(f"   First record: {records[0]}")
    
    print("\n" + "="*70)
    print("✅ CSV OPERATIONS COMPLETE")
    print("="*70)