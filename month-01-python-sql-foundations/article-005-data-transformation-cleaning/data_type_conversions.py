# data_type_conversions.py - Data Type Conversions and Fixes

import pandas as pd
import numpy as np
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


def create_mixed_type_dataset():
    """Create dataset with incorrect data types"""
    
    data = {
        'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'age': ['28', '35', '42', 'unknown', '31'],  # Should be numeric
        'salary': ['1200000', '900000', '1.5M', '800K', '1100000'],  # Mixed formats
        'join_date': ['2023-01-15', '15/02/2023', '2023.03.20', '2023-04-25', 'Apr 30, 2023'],  # Mixed date formats
        'is_active': ['Yes', 'No', 'True', '1', '0'],  # Should be boolean
        'purchase_amount': ['₹50,000', '75000', '₹1,20,000', '85000', '₹95,000'],  # Currency symbols
        'phone': [9876543210, 8765432109, 7654321098, 6543210987, 5432109876],  # Should be string
        'rating': ['4.5', '3.8', '5.0', '4.2', 'N/A']  # Should be float
    }
    
    df = pd.DataFrame(data)
    df.to_csv('mixed_type_data.csv', index=False)
    
    print(f"{Fore.GREEN}✅ Created mixed type dataset: mixed_type_data.csv{Style.RESET_ALL}\n")
    return df


def analyze_data_types(df):
    """Analyze current data types"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔍 DATA TYPE ANALYSIS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("Current Data Types:")
    print(df.dtypes)
    print()
    
    print("Sample Data:")
    print(df.head())
    print()
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum() / 1024
    print(f"Memory Usage: {memory_usage:.2f} KB")
    print()


def convert_numeric_types(df):
    """Convert string columns to numeric types"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔢 CONVERTING TO NUMERIC TYPES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_converted = df.copy()
    
    # Convert age to numeric (coerce errors to NaN)
    print("1. Converting 'age' column:")
    print(f"   Original type: {df_converted['age'].dtype}")
    df_converted['age'] = pd.to_numeric(df_converted['age'], errors='coerce')
    print(f"   New type: {df_converted['age'].dtype}")
    print(f"   Values: {df_converted['age'].tolist()}")
    print()
    
    # Convert salary (handle K and M suffixes)
    print("2. Converting 'salary' column (with K/M handling):")
    print(f"   Original values: {df_converted['salary'].tolist()}")
    
    def parse_salary(value):
        """Parse salary with K/M suffixes"""
        if pd.isna(value):
            return np.nan
        
        value = str(value).strip()
        
        # Remove currency symbols and commas
        value = value.replace('₹', '').replace(',', '').strip()
        
        # Handle K (thousands)
        if value.endswith('K'):
            return float(value[:-1]) * 1000
        
        # Handle M (millions)
        if value.endswith('M'):
            return float(value[:-1]) * 1000000
        
        # Regular number
        try:
            return float(value)
        except:
            return np.nan
    
    df_converted['salary'] = df_converted['salary'].apply(parse_salary)
    print(f"   New type: {df_converted['salary'].dtype}")
    print(f"   Values: {df_converted['salary'].tolist()}")
    print()
    
    # Convert purchase_amount (remove currency symbols)
    print("3. Converting 'purchase_amount' column:")
    print(f"   Original values: {df_converted['purchase_amount'].tolist()}")
    
    df_converted['purchase_amount'] = (
        df_converted['purchase_amount']
        .str.replace('₹', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(float)
    )
    print(f"   New type: {df_converted['purchase_amount'].dtype}")
    print(f"   Values: {df_converted['purchase_amount'].tolist()}")
    print()
    
    # Convert rating to float
    print("4. Converting 'rating' column:")
    print(f"   Original values: {df_converted['rating'].tolist()}")
    df_converted['rating'] = pd.to_numeric(df_converted['rating'], errors='coerce')
    print(f"   New type: {df_converted['rating'].dtype}")
    print(f"   Values: {df_converted['rating'].tolist()}")
    print()
    
    return df_converted


def convert_date_types(df):
    """Convert string columns to datetime"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📅 CONVERTING TO DATETIME TYPES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_converted = df.copy()
    
    print("Converting 'join_date' column:")
    print(f"Original values: {df_converted['join_date'].tolist()}")
    print()
    
    # Try multiple date formats
    date_formats = [
        '%Y-%m-%d',      # 2023-01-15
        '%d/%m/%Y',      # 15/02/2023
        '%Y.%m.%d',      # 2023.03.20
        '%b %d, %Y'      # Apr 30, 2023
    ]
    
    def parse_date(date_str):
        """Try parsing with multiple formats"""
        for fmt in date_formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        
        # If all formats fail, use pandas' flexible parser
        try:
            return pd.to_datetime(date_str)
        except:
            return pd.NaT
    
    df_converted['join_date'] = df_converted['join_date'].apply(parse_date)
    
    print(f"New type: {df_converted['join_date'].dtype}")
    print(f"Converted values:")
    print(df_converted['join_date'])
    print()
    
    # Extract date components
    df_converted['join_year'] = df_converted['join_date'].dt.year
    df_converted['join_month'] = df_converted['join_date'].dt.month
    df_converted['join_day'] = df_converted['join_date'].dt.day
    df_converted['join_weekday'] = df_converted['join_date'].dt.day_name()
    
    print("Extracted date components:")
    print(df_converted[['join_date', 'join_year', 'join_month', 'join_day', 'join_weekday']])
    print()
    
    return df_converted


def convert_boolean_types(df):
    """Convert string columns to boolean"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"✅ CONVERTING TO BOOLEAN TYPES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_converted = df.copy()
    
    print("Converting 'is_active' column:")
    print(f"Original values: {df_converted['is_active'].tolist()}")
    
    # Define mapping for boolean conversion
    bool_mapping = {
        'Yes': True, 'yes': True, 'YES': True,
        'No': False, 'no': False, 'NO': False,
        'True': True, 'true': True, 'TRUE': True,
        'False': False, 'false': False, 'FALSE': False,
        '1': True, '0': False,
        1: True, 0: False
    }
    
    df_converted['is_active'] = df_converted['is_active'].map(bool_mapping)
    
    print(f"New type: {df_converted['is_active'].dtype}")
    print(f"Converted values: {df_converted['is_active'].tolist()}")
    print()
    
    return df_converted


def convert_string_types(df):
    """Convert numeric columns to string (for IDs, phone numbers)"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📝 CONVERTING TO STRING TYPES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_converted = df.copy()
    
    print("Converting 'phone' column to string:")
    print(f"Original type: {df_converted['phone'].dtype}")
    print(f"Original values: {df_converted['phone'].tolist()}")
    
    # Convert to string and format
    df_converted['phone'] = df_converted['phone'].astype(str)
    
    # Ensure 10 digits (pad with zeros if needed)
    df_converted['phone'] = df_converted['phone'].str.zfill(10)
    
    print(f"New type: {df_converted['phone'].dtype}")
    print(f"Formatted values: {df_converted['phone'].tolist()}")
    print()
    
    return df_converted


def optimize_data_types(df):
    """Optimize data types to reduce memory usage"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"⚡ OPTIMIZING DATA TYPES FOR MEMORY")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_optimized = df.copy()
    
    # Original memory usage
    original_memory = df_optimized.memory_usage(deep=True).sum() / 1024
    print(f"Original memory usage: {original_memory:.2f} KB")
    print()
    
    # Optimize integer columns
    for col in df_optimized.select_dtypes(include=['int64']).columns:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
        print(f"✅ Optimized {col}: int64 → {df_optimized[col].dtype}")
    
    # Optimize float columns
    for col in df_optimized.select_dtypes(include=['float64']).columns:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
        print(f"✅ Optimized {col}: float64 → {df_optimized[col].dtype}")
    
    # Convert object columns to category (if low cardinality)
    for col in df_optimized.select_dtypes(include=['object']).columns:
        num_unique = df_optimized[col].nunique()
        num_total = len(df_optimized[col])
        
        # If less than 50% unique values, convert to category
        if num_unique / num_total < 0.5:
            df_optimized[col] = df_optimized[col].astype('category')
            print(f"✅ Optimized {col}: object → category")
    
    # New memory usage
    new_memory = df_optimized.memory_usage(deep=True).sum() / 1024
    savings = ((original_memory - new_memory) / original_memory) * 100
    
    print()
    print(f"New memory usage: {new_memory:.2f} KB")
    print(f"Memory saved: {savings:.1f}%")
    print()
    
    return df_optimized


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{'='*70}")
    print(f"🔤 DATA TYPE CONVERSION DEMONSTRATION")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create mixed type dataset
    df = create_mixed_type_dataset()
    
    # Analyze original types
    analyze_data_types(df)
    
    # Convert numeric types
    df = convert_numeric_types(df)
    
    # Convert date types
    df = convert_date_types(df)
    
    # Convert boolean types
    df = convert_boolean_types(df)
    
    # Convert string types
    df = convert_string_types(df)
    
    # Optimize data types
    df_optimized = optimize_data_types(df)
    
    # Save results
    df.to_csv('output/converted_data_types.csv', index=False)
    df_optimized.to_parquet('output/optimized_data.parquet', index=False)
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"✅ DATA TYPE CONVERSION COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}")