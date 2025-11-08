
import pandas as pd
import numpy as np
import os
from colorama import Fore, Style, init

init(autoreset=True)


def create_messy_dataset():
    """Create a dataset with various missing value patterns"""
    
    data = {
        'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008'],
        'name': ['Mayurkumar Surani', 'Rahul Sharma', None, 'Priya Patel', '', 'Amit Kumar', 'Sneha Desai', np.nan],
        'email': ['mayur@example.com', None, 'priya@example.com', 'amit@example.com', '', 'sneha@example.com', 'invalid', np.nan],
        'phone': ['9876543210', '8765432109', None, '7654321098', '', '6543210987', '5432109876', np.nan],
        'age': [28, 35, np.nan, 42, 25, np.nan, 31, 29],
        'salary': [1200000, 900000, np.nan, 1500000, 800000, np.nan, 1100000, 950000],
        'city': ['Pune', 'Mumbai', 'Bangalore', None, 'Pune', 'Delhi', '', 'Mumbai'],
        'purchase_amount': [50000, np.nan, 75000, 120000, np.nan, 85000, 95000, 110000]
    }
    
    df = pd.DataFrame(data)
    df.to_csv('messy_customer_data.csv', index=False)
    
    print(f"{Fore.GREEN}✅ Created messy dataset: messy_customer_data.csv{Style.RESET_ALL}\n")
    return df


def analyze_missing_values(df):
    """Analyze missing values in dataset"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔍 MISSING VALUES ANALYSIS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Count missing values
    missing_counts = df.isnull().sum()
    missing_percentages = (df.isnull().sum() / len(df)) * 100
    
    # Create summary DataFrame
    missing_summary = pd.DataFrame({
        'Column': missing_counts.index,
        'Missing Count': missing_counts.values,
        'Missing %': missing_percentages.values
    })
    
    # Filter columns with missing values
    missing_summary = missing_summary[missing_summary['Missing Count'] > 0]
    missing_summary = missing_summary.sort_values('Missing Count', ascending=False)
    
    print("Missing Values Summary:")
    print(missing_summary.to_string(index=False))
    print()
    
    # Total missing values
    total_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    missing_pct = (total_missing / total_cells) * 100
    
    print(f"Total Missing Values: {total_missing} ({missing_pct:.2f}% of all data)")
    print()
    
    return missing_summary


def handle_missing_numeric(df):
    """Handle missing values in numeric columns"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔢 HANDLING NUMERIC MISSING VALUES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_cleaned = df.copy()
    
    # Strategy 1: Fill with mean (for normally distributed data)
    if 'age' in df_cleaned.columns:
        mean_age = df_cleaned['age'].mean()
        df_cleaned['age_mean_filled'] = df_cleaned['age'].fillna(mean_age)
        print(f"✅ Age: Filled with mean ({mean_age:.1f})")
    
    # Strategy 2: Fill with median (for skewed data)
    if 'salary' in df_cleaned.columns:
        median_salary = df_cleaned['salary'].median()
        df_cleaned['salary_median_filled'] = df_cleaned['salary'].fillna(median_salary)
        print(f"✅ Salary: Filled with median (₹{median_salary:,.0f})")
    
    # Strategy 3: Fill with mode (most common value)
    if 'purchase_amount' in df_cleaned.columns:
        mode_purchase = df_cleaned['purchase_amount'].mode()[0] if not df_cleaned['purchase_amount'].mode().empty else 0
        df_cleaned['purchase_mode_filled'] = df_cleaned['purchase_amount'].fillna(mode_purchase)
        print(f"✅ Purchase Amount: Filled with mode (₹{mode_purchase:,.0f})")
    
    # Strategy 4: Forward fill (use previous value)
    df_cleaned['age_ffill'] = df_cleaned['age'].ffill()
    print(f"✅ Age: Forward filled (use previous row's value)")
    
    # Strategy 5: Backward fill (use next value)
    df_cleaned['age_bfill'] = df_cleaned['age'].bfill()
    print(f"✅ Age: Backward filled (use next row's value)")
    
    print()
    return df_cleaned


def handle_missing_categorical(df):
    """Handle missing values in categorical columns"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📝 HANDLING CATEGORICAL MISSING VALUES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_cleaned = df.copy()
    
    # Strategy 1: Fill with mode (most common value)
    if 'city' in df_cleaned.columns:
        mode_city = df_cleaned['city'].mode()[0] if not df_cleaned['city'].mode().empty else 'Unknown'
        df_cleaned['city_mode_filled'] = df_cleaned['city'].fillna(mode_city)
        print(f"✅ City: Filled with mode ('{mode_city}')")
    
    # Strategy 2: Fill with constant value
    df_cleaned['name_filled'] = df_cleaned['name'].fillna('Unknown Customer')
    print(f"✅ Name: Filled with 'Unknown Customer'")
    
    # Strategy 3: Fill with empty string (for optional fields)
    df_cleaned['email_filled'] = df_cleaned['email'].fillna('')
    print(f"✅ Email: Filled with empty string")
    
    # Strategy 4: Create 'Missing' category
    df_cleaned['city_with_missing'] = df_cleaned['city'].fillna('Missing')
    print(f"✅ City: Created 'Missing' category")
    
    print()
    return df_cleaned


def drop_missing_values(df):
    """Demonstrate dropping rows/columns with missing values"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🗑️  DROPPING MISSING VALUES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"Original shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Drop rows with ANY missing value
    df_dropna_any = df.dropna()
    print(f"\n1. Drop rows with ANY missing value:")
    print(f"   Result: {df_dropna_any.shape[0]} rows × {df_dropna_any.shape[1]} columns")
    print(f"   Rows dropped: {df.shape[0] - df_dropna_any.shape[0]}")
    
    # Drop rows with ALL values missing
    df_dropna_all = df.dropna(how='all')
    print(f"\n2. Drop rows with ALL values missing:")
    print(f"   Result: {df_dropna_all.shape[0]} rows × {df_dropna_all.shape[1]} columns")
    print(f"   Rows dropped: {df.shape[0] - df_dropna_all.shape[0]}")
    
    # Drop rows with missing values in specific columns
    df_dropna_subset = df.dropna(subset=['name', 'email'])
    print(f"\n3. Drop rows with missing name OR email:")
    print(f"   Result: {df_dropna_subset.shape[0]} rows × {df_dropna_subset.shape[1]} columns")
    print(f"   Rows dropped: {df.shape[0] - df_dropna_subset.shape[0]}")
    
    # Drop columns with too many missing values (>50%)
    threshold = len(df) * 0.5
    df_drop_cols = df.dropna(axis=1, thresh=threshold)
    print(f"\n4. Drop columns with >50% missing values:")
    print(f"   Result: {df_drop_cols.shape[0]} rows × {df_drop_cols.shape[1]} columns")
    print(f"   Columns dropped: {df.shape[1] - df_drop_cols.shape[1]}")
    
    print()


def interpolate_missing_values(df):
    """Interpolate missing values (for time series or ordered data)"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📈 INTERPOLATING MISSING VALUES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create time series data with missing values
    dates = pd.date_range('2025-01-01', periods=10)
    sales = [100, 120, np.nan, 150, np.nan, 180, 200, np.nan, 240, 260]
    
    df_ts = pd.DataFrame({
        'date': dates,
        'sales': sales
    })
    
    print("Original time series data:")
    print(df_ts)
    print()
    
    # Linear interpolation
    df_ts['sales_linear'] = df_ts['sales'].interpolate(method='linear')
    print("After linear interpolation:")
    print(df_ts[['date', 'sales', 'sales_linear']])
    print()
    
    # Polynomial interpolation
    df_ts['sales_polynomial'] = df_ts['sales'].interpolate(method='polynomial', order=2)
    print("After polynomial interpolation:")
    print(df_ts[['date', 'sales', 'sales_polynomial']])
    print()


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{'='*70}")
    print(f"🧹 MISSING VALUES HANDLING DEMONSTRATION")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create messy dataset
    df = create_messy_dataset()
    
    print("Original Dataset:")
    print(df)
    print()
    
    # Analyze missing values
    analyze_missing_values(df)
    
    # Handle numeric missing values
    df_numeric = handle_missing_numeric(df)
    
    # Handle categorical missing values
    df_categorical = handle_missing_categorical(df)
    
    # Demonstrate dropping
    drop_missing_values(df)
    
    # Demonstrate interpolation
    interpolate_missing_values(df)
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save cleaned data
    df_numeric.to_csv('output/cleaned_numeric.csv', index=False)
    df_categorical.to_csv('output/cleaned_categorical.csv', index=False)
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"✅ MISSING VALUES HANDLING COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}")