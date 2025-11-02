# excel_operations.py - Excel File Operations

import pandas as pd
import openpyxl
from datetime import datetime
import os


def read_excel_pandas(file_path, sheet_name=0):
    """
    Read Excel file using pandas
    
    Args:
        file_path (str): Path to Excel file
        sheet_name (str/int): Sheet name or index
        
    Returns:
        pd.DataFrame: Loaded data
    """
    try:
        print(f"📂 Reading Excel: {file_path}")
        print(f"   Sheet: {sheet_name}")
        
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
        
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"   Columns: {', '.join(df.columns)}\n")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def read_all_sheets(file_path):
    """
    Read all sheets from Excel file
    
    Args:
        file_path (str): Path to Excel file
        
    Returns:
        dict: Dictionary of DataFrames (sheet_name: df)
    """
    try:
        print(f"📂 Reading all sheets from: {file_path}")
        
        # Read all sheets
        sheets_dict = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        
        print(f"✅ Found {len(sheets_dict)} sheets:")
        for sheet_name, df in sheets_dict.items():
            print(f"   - {sheet_name}: {len(df)} rows")
        print()
        
        return sheets_dict
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}


def write_excel_pandas(df, file_path, sheet_name='Sheet1'):
    """
    Write DataFrame to Excel
    
    Args:
        df (pd.DataFrame): Data to write
        file_path (str): Output file path
        sheet_name (str): Sheet name
    """
    try:
        print(f"💾 Writing Excel: {file_path}")
        
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        df.to_excel(file_path, sheet_name=sheet_name, index=False, engine='openpyxl')
        
        file_size = os.path.getsize(file_path) / 1024
        print(f"✅ Saved {len(df)} rows ({file_size:.2f} KB)\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def write_multiple_sheets(data_dict, file_path):
    """
    Write multiple DataFrames to different sheets
    
    Args:
        data_dict (dict): Dictionary of DataFrames (sheet_name: df)
        file_path (str): Output file path
    """
    try:
        print(f"💾 Writing multiple sheets to: {file_path}")
        
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"   - {sheet_name}: {len(df)} rows")
        
        file_size = os.path.getsize(file_path) / 1024
        print(f"✅ Saved {len(data_dict)} sheets ({file_size:.2f} KB)\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def create_sample_excel():
    """Create sample Excel files for testing"""
    
    # Sample 1: Single sheet
    sales_data = {
        'Date': pd.date_range('2025-01-01', periods=10),
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'] * 2,
        'Price': [75000, 500, 1500, 25000, 2000] * 2,
        'Quantity': [2, 10, 5, 1, 4] * 2,
        'Region': ['West', 'East', 'North', 'South', 'West'] * 2
    }
    
    df_sales = pd.DataFrame(sales_data)
    df_sales['Revenue'] = df_sales['Price'] * df_sales['Quantity']
    df_sales.to_excel('sample_sales.xlsx', index=False, engine='openpyxl')
    print("✅ Created: sample_sales.xlsx")
    
    # Sample 2: Multiple sheets
    customers = pd.DataFrame({
        'CustomerID': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'Name': ['Mayurkumar', 'Rahul', 'Priya', 'Amit', 'Sneha'],
        'City': ['Pune', 'Mumbai', 'Bangalore', 'Delhi', 'Pune'],
        'Segment': ['Premium', 'Gold', 'Premium', 'Silver', 'Gold']
    })
    
    products = pd.DataFrame({
        'ProductID': ['P001', 'P002', 'P003', 'P004'],
        'Name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
        'Category': ['Electronics'] * 4,
        'Price': [75000, 500, 1500, 25000]
    })
    
    with pd.ExcelWriter('multi_sheet.xlsx', engine='openpyxl') as writer:
        customers.to_excel(writer, sheet_name='Customers', index=False)
        products.to_excel(writer, sheet_name='Products', index=False)
        df_sales.to_excel(writer, sheet_name='Sales', index=False)
    
    print("✅ Created: multi_sheet.xlsx (3 sheets)\n")


if __name__ == "__main__":
    print("="*70)
    print("📊 EXCEL OPERATIONS DEMONSTRATION")
    print("="*70 + "\n")
    
    # Create sample files
    create_sample_excel()
    
    # Read single sheet
    print("1. Read Single Sheet:")
    df = read_excel_pandas('sample_sales.xlsx')
    if df is not None:
        print(df.head())
    print()
    
    # Read all sheets
    print("2. Read All Sheets:")
    sheets = read_all_sheets('multi_sheet.xlsx')
    if sheets:
        print("   Customers sheet:")
        print(sheets['Customers'].head())
    print()
    
    # Write Excel
    print("3. Write Excel:")
    if df is not None:
        # Add summary statistics
        summary = df.groupby('Product').agg({
            'Quantity': 'sum',
            'Revenue': 'sum'
        }).reset_index()
        
        write_excel_pandas(summary, 'output/product_summary.xlsx', sheet_name='Summary')
    
    # Write multiple sheets
    print("4. Write Multiple Sheets:")
    if df is not None:
        by_region = df.groupby('Region').agg({
            'Revenue': 'sum'
        }).reset_index()
        
        by_product = df.groupby('Product').agg({
            'Revenue': 'sum'
        }).reset_index()
        
        write_multiple_sheets({
            'By Region': by_region,
            'By Product': by_product,
            'Raw Data': df
        }, 'output/analysis.xlsx')
    
    print("="*70)
    print("✅ EXCEL OPERATIONS COMPLETE")
    print("="*70)