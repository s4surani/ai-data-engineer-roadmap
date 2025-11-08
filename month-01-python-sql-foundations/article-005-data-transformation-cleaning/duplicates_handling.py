# duplicates_handling.py - Handling Duplicate Records

import pandas as pd
import numpy as np
from colorama import Fore, Style, init

init(autoreset=True)


def create_dataset_with_duplicates():
    """Create dataset with various types of duplicates"""
    
    data = {
        'customer_id': ['C001', 'C001', 'C002', 'C003', 'C003', 'C003', 'C004', 'C005', 'C005'],
        'name': ['Mayurkumar Surani', 'Mayurkumar Surani', 'Rahul Sharma', 
                 'Priya Patel', 'Priya Patel', 'PRIYA PATEL', 
                 'Amit Kumar', 'Sneha Desai', 'Sneha Desai'],
        'email': ['mayur@example.com', 'mayur@example.com', 'rahul@example.com',
                  'priya@example.com', 'priya@example.com', 'priya@example.com',
                  'amit@example.com', 'sneha@example.com', 'SNEHA@EXAMPLE.COM'],
        'phone': ['9876543210', '9876543210', '8765432109',
                  '7654321098', '7654321098', '7654321098',
                  '6543210987', '5432109876', '5432109876'],
        'purchase_date': ['2025-01-01', '2025-01-01', '2025-01-02',
                          '2025-01-03', '2025-01-03', '2025-01-04',
                          '2025-01-05', '2025-01-06', '2025-01-06'],
        'amount': [50000, 50000, 75000, 120000, 120000, 95000, 85000, 110000, 110000]
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data_with_duplicates.csv', index=False)
    
    print(f"{Fore.GREEN}✅ Created dataset with duplicates: data_with_duplicates.csv{Style.RESET_ALL}\n")
    return df


def analyze_duplicates(df):
    """Analyze duplicate records"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔍 DUPLICATE ANALYSIS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Check for exact duplicates (all columns)
    exact_duplicates = df.duplicated().sum()
    print(f"1. Exact Duplicates (all columns match):")
    print(f"   Count: {exact_duplicates}")
    
    if exact_duplicates > 0:
        print(f"\n   Duplicate rows:")
        print(df[df.duplicated(keep=False)].sort_values('customer_id'))
    print()
    
    # Check duplicates based on specific columns
    id_duplicates = df.duplicated(subset=['customer_id']).sum()
    print(f"2. Duplicate Customer IDs:")
    print(f"   Count: {id_duplicates}")
    
    if id_duplicates > 0:
        print(f"\n   Customers with multiple records:")
        duplicate_ids = df[df.duplicated(subset=['customer_id'], keep=False)]
        print(duplicate_ids[['customer_id', 'name', 'purchase_date', 'amount']].sort_values('customer_id'))
    print()
    
    # Check duplicates based on multiple columns
    combo_duplicates = df.duplicated(subset=['customer_id', 'purchase_date']).sum()
    print(f"3. Duplicate Customer ID + Purchase Date:")
    print(f"   Count: {combo_duplicates}")
    print()
    
    return {
        'exact': exact_duplicates,
        'customer_id': id_duplicates,
        'combo': combo_duplicates
    }


def remove_exact_duplicates(df):
    """Remove exact duplicate rows"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🗑️  REMOVING EXACT DUPLICATES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"Original shape: {df.shape[0]} rows")
    
    # Keep first occurrence
    df_first = df.drop_duplicates(keep='first')
    print(f"\n1. Keep FIRST occurrence:")
    print(f"   Result: {df_first.shape[0]} rows")
    print(f"   Removed: {df.shape[0] - df_first.shape[0]} duplicates")
    
    # Keep last occurrence
    df_last = df.drop_duplicates(keep='last')
    print(f"\n2. Keep LAST occurrence:")
    print(f"   Result: {df_last.shape[0]} rows")
    print(f"   Removed: {df.shape[0] - df_last.shape[0]} duplicates")
    
    # Remove all duplicates (keep none)
    df_none = df.drop_duplicates(keep=False)
    print(f"\n3. Remove ALL duplicates (keep none):")
    print(f"   Result: {df_none.shape[0]} rows")
    print(f"   Removed: {df.shape[0] - df_none.shape[0]} rows")
    
    print()
    return df_first


def remove_duplicates_by_column(df):
    """Remove duplicates based on specific columns"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🎯 REMOVING DUPLICATES BY SPECIFIC COLUMNS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"Original shape: {df.shape[0]} rows")
    
    # Remove duplicates based on customer_id (keep first)
    df_unique_customers = df.drop_duplicates(subset=['customer_id'], keep='first')
    print(f"\n1. Unique customers (by customer_id):")
    print(f"   Result: {df_unique_customers.shape[0]} rows")
    print(f"   Removed: {df.shape[0] - df_unique_customers.shape[0]} duplicates")
    
    # Remove duplicates based on email (case-insensitive)
    df['email_lower'] = df['email'].str.lower()
    df_unique_emails = df.drop_duplicates(subset=['email_lower'], keep='first')
    print(f"\n2. Unique emails (case-insensitive):")
    print(f"   Result: {df_unique_emails.shape[0]} rows")
    print(f"   Removed: {df.shape[0] - df_unique_emails.shape[0]} duplicates")
    
    # Remove duplicates based on multiple columns
    df_unique_combo = df.drop_duplicates(subset=['customer_id', 'purchase_date'], keep='first')
    print(f"\n3. Unique customer + date combinations:")
    print(f"   Result: {df_unique_combo.shape[0]} rows")
    print(f"   Removed: {df.shape[0] - df_unique_combo.shape[0]} duplicates")
    
    print()
    return df_unique_customers


def smart_duplicate_handling(df):
    """Intelligently handle duplicates by aggregating"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🧠 SMART DUPLICATE HANDLING (AGGREGATION)")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("Strategy: Instead of removing duplicates, aggregate them!")
    print()
    
    # Group by customer and aggregate
    df_aggregated = df.groupby('customer_id').agg({
        'name': 'first',  # Take first name
        'email': 'first',  # Take first email
        'phone': 'first',  # Take first phone
        'purchase_date': 'count',  # Count purchases
        'amount': ['sum', 'mean', 'max']  # Multiple aggregations
    }).reset_index()
    
    # Flatten column names
    df_aggregated.columns = ['customer_id', 'name', 'email', 'phone', 
                             'purchase_count', 'total_amount', 'avg_amount', 'max_amount']
    
    print("Aggregated Customer Summary:")
    print(df_aggregated)
    print()
    
    print(f"✅ Converted {df.shape[0]} rows into {df_aggregated.shape[0]} unique customers")
    print(f"   with aggregated purchase information")
    print()
    
    return df_aggregated


def find_fuzzy_duplicates(df):
    """Find potential duplicates with slight variations"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔎 FINDING FUZZY DUPLICATES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("Looking for records that are 'almost' duplicates...")
    print("(same customer_id but different name cases)")
    print()
    
    # Normalize names for comparison
    df['name_normalized'] = df['name'].str.lower().str.strip()
    
    # Find customer IDs with multiple name variations
    name_variations = df.groupby('customer_id')['name_normalized'].nunique()
    fuzzy_customers = name_variations[name_variations > 1].index.tolist()
    
    if fuzzy_customers:
        print(f"Found {len(fuzzy_customers)} customers with name variations:")
        for cid in fuzzy_customers:
            customer_records = df[df['customer_id'] == cid][['customer_id', 'name', 'email']]
            print(f"\n{cid}:")
            print(customer_records.to_string(index=False))
    else:
        print("No fuzzy duplicates found!")
    
    print()


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{'='*70}")
    print(f"🔄 DUPLICATE HANDLING DEMONSTRATION")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create dataset with duplicates
    df = create_dataset_with_duplicates()
    
    print("Original Dataset:")
    print(df)
    print()
    
    # Analyze duplicates
    dup_stats = analyze_duplicates(df)
    
    # Remove exact duplicates
    df_no_exact = remove_exact_duplicates(df)
    
    # Remove duplicates by column
    df_unique = remove_duplicates_by_column(df)
    
    # Smart aggregation
    df_aggregated = smart_duplicate_handling(df)
    
    # Find fuzzy duplicates
    find_fuzzy_duplicates(df)
    
    # Save results
    df_no_exact.to_csv('output/no_exact_duplicates.csv', index=False)
    df_unique.to_csv('output/unique_customers.csv', index=False)
    df_aggregated.to_csv('output/aggregated_customers.csv', index=False)
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"✅ DUPLICATE HANDLING COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}")