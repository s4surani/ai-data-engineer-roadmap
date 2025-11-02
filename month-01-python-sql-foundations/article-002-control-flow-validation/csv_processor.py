# csv_processor.py - Real-world CSV Processing

import pandas as pd
from datetime import datetime

def process_sales_file(file_path):
    """
    Process sales CSV file with validation
    
    Args:
        file_path (str): Path to CSV file
    """
    print(f"📂 Loading {file_path}...")
    df = pd.read_csv(file_path)
    print(f"✅ Loaded {len(df)} records\n")
    
    print("="*60)
    print("🔄 PROCESSING RECORDS")
    print("="*60 + "\n")
    
    valid_records = []
    invalid_records = []
    total_revenue = 0
    
    # Process each row
    for index, row in df.iterrows():
        record_num = index + 1
        
        # Calculate revenue
        revenue = row['price'] * row['quantity']
        
        # Validation checks
        is_valid = True
        errors = []
        
        if row['price'] <= 0:
            is_valid = False
            errors.append("Invalid price")
        
        if row['quantity'] <= 0:
            is_valid = False
            errors.append("Invalid quantity")
        
        if pd.isna(row['customer_id']):
            is_valid = False
            errors.append("Missing customer_id")
        
        # Display progress every 100 records
        if record_num % 100 == 0:
            print(f"  Processed {record_num} records...")
        
        if is_valid:
            valid_records.append(row.to_dict())
            total_revenue += revenue
        else:
            invalid_records.append({
                'record_num': record_num,
                'data': row.to_dict(),
                'errors': errors
            })
    
    print(f"\n✅ Processing complete!\n")
    
    # Summary report
    print("="*60)
    print("📊 PROCESSING SUMMARY")
    print("="*60)
    print(f"Total Records: {len(df)}")
    print(f"Valid Records: {len(valid_records)} ({len(valid_records)/len(df)*100:.1f}%)")
    print(f"Invalid Records: {len(invalid_records)} ({len(invalid_records)/len(df)*100:.1f}%)")
    print(f"Total Revenue: ₹{total_revenue:,.2f}")
    print("="*60 + "\n")
    
    # Show invalid records
    if invalid_records:
        print("❌ INVALID RECORDS:")
        for record in invalid_records[:5]:  # Show first 5
            print(f"\n  Record #{record['record_num']}:")
            print(f"    Product: {record['data'].get('product', 'N/A')}")
            print(f"    Errors: {', '.join(record['errors'])}")
        
        if len(invalid_records) > 5:
            print(f"\n  ... and {len(invalid_records) - 5} more invalid records")
    
    return valid_records, invalid_records

# Create sample data with some invalid records
sample_data = {
    'date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05'],
    'product': ['Laptop', 'Mouse', '', 'Monitor', 'Keyboard'],
    'price': [75000, -500, 1500, 25000, 1500],
    'quantity': [2, 5, 0, 1, 3],
    'customer_id': ['C001', 'C002', 'C003', None, 'C005'],
    'region': ['West', 'East', 'North', 'South', 'West']
}

df = pd.DataFrame(sample_data)
df.to_csv('sample_sales_with_errors.csv', index=False)

# Process the file
valid, invalid = process_sales_file('sample_sales_with_errors.csv')