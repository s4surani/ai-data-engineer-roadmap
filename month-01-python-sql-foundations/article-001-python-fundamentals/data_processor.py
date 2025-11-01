# data_processor.py - Your First Data Engineering Script

import pandas as pd
from datetime import datetime

def load_data(file_path):
    """
    Load CSV data into a Pandas DataFrame
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    print(f"📂 Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    print(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns\n")
    return df

def explore_data(df):
    """
    Perform basic data exploration
    
    Args:
        df (pd.DataFrame): Input dataframe
    """
    print("="*60)
    print("📊 DATA EXPLORATION")
    print("="*60)
    
    # Display first few rows
    print("\n🔍 First 5 rows:")
    print(df.head())
    
    # Display data types
    print("\n📋 Column Data Types:")
    print(df.dtypes)
    
    # Display basic statistics
    print("\n📈 Numerical Statistics:")
    print(df.describe())
    
    # Check for missing values
    print("\n❓ Missing Values:")
    print(df.isnull().sum())
    
    print("\n" + "="*60 + "\n")

def analyze_sales(df):
    """
    Perform sales analysis
    
    Args:
        df (pd.DataFrame): Sales dataframe
    """
    print("="*60)
    print("💰 SALES ANALYSIS")
    print("="*60)
    
    # Calculate total revenue
    df['revenue'] = df['quantity'] * df['price']
    
    # Total metrics
    total_revenue = df['revenue'].sum()
    total_quantity = df['quantity'].sum()
    total_orders = len(df)
    
    print(f"\n📊 Overall Metrics:")
    print(f"Total Revenue: ₹{total_revenue:,}")
    print(f"Total Quantity Sold: {total_quantity:,} units")
    print(f"Total Orders: {total_orders}")
    print(f"Average Order Value: ₹{total_revenue/total_orders:,.2f}")
    
    # Product analysis
    print(f"\n🏆 Top Products by Revenue:")
    product_revenue = df.groupby('product')['revenue'].sum().sort_values(ascending=False)
    for product, revenue in product_revenue.items():
        print(f"  {product}: ₹{revenue:,}")
    
    # Region analysis
    print(f"\n🌍 Revenue by Region:")
    region_revenue = df.groupby('region')['revenue'].sum().sort_values(ascending=False)
    for region, revenue in region_revenue.items():
        print(f"  {region}: ₹{revenue:,}")
    
    # Customer analysis
    print(f"\n👥 Top Customers:")
    customer_revenue = df.groupby('customer_id')['revenue'].sum().sort_values(ascending=False).head(3)
    for customer, revenue in customer_revenue.items():
        print(f"  {customer}: ₹{revenue:,}")
    
    print("\n" + "="*60 + "\n")

def save_summary(df, output_file):
    """
    Save analysis summary to CSV
    
    Args:
        df (pd.DataFrame): Analyzed dataframe
        output_file (str): Output file path
    """
    print(f"💾 Saving summary to {output_file}...")
    
    # Create summary dataframe
    summary = df.groupby('product').agg({
        'quantity': 'sum',
        'revenue': 'sum',
        'customer_id': 'count'
    }).rename(columns={'customer_id': 'order_count'})
    
    summary['avg_order_value'] = summary['revenue'] / summary['order_count']
    summary = summary.sort_values('revenue', ascending=False)
    
    # Save to CSV
    summary.to_csv(output_file)
    print(f"✅ Summary saved successfully!\n")
    
    return summary

def main():
    """
    Main execution function
    """
    print("\n" + "="*60)
    print("🚀 DATA PROCESSING PIPELINE STARTED")
    print("="*60 + "\n")
    
    # Step 1: Load data
    df = load_data('sample_sales.csv')
    
    # Step 2: Explore data
    explore_data(df)
    
    # Step 3: Analyze sales
    analyze_sales(df)
    
    # Step 4: Save summary
    summary = save_summary(df, 'sales_summary.csv')
    
    print("="*60)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"\nGenerated files:")
    print("  📄 sales_summary.csv - Product-wise summary")
    print(f"\nExecution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n")

if __name__ == "__main__":
    main()