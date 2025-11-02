# production_validator.py - Production-Grade Data Validation Pipeline

import pandas as pd
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class DataValidator:
    """
    Production-grade data validation pipeline
    """
    
    def __init__(self, config=None):
        """
        Initialize validator with configuration
        
        Args:
            config (dict): Validation rules configuration
        """
        self.config = config or self.get_default_config()
        self.validation_results = {
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'errors': [],
            'warnings': []
        }
    
    @staticmethod
    def get_default_config():
        """Get default validation rules"""
        return {
            'price_min': 0,
            'price_max': 1000000,
            'quantity_min': 1,
            'quantity_max': 10000,
            'valid_regions': ['North', 'South', 'East', 'West'],
            'required_fields': ['product', 'price', 'quantity', 'customer_id', 'region'],
            'high_value_threshold': 500000
        }
    
    def validate_record(self, record, record_num):
        """
        Validate a single record
        
        Args:
            record (dict): Record to validate
            record_num (int): Record number
            
        Returns:
            tuple: (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        # Check required fields
        for field in self.config['required_fields']:
            if field not in record or pd.isna(record[field]) or record[field] == '':
                errors.append(f"Missing required field: {field}")
        
        # If critical fields missing, return early
        if errors:
            return False, errors, warnings
        
        # Validate price
        price = record['price']
        if price < self.config['price_min']:
            errors.append(f"Price below minimum: ₹{price}")
        elif price > self.config['price_max']:
            errors.append(f"Price above maximum: ₹{price:,}")
        
        # Validate quantity
        quantity = record['quantity']
        if quantity < self.config['quantity_min']:
            errors.append(f"Quantity below minimum: {quantity}")
        elif quantity > self.config['quantity_max']:
            warnings.append(f"Unusually high quantity: {quantity}")
        
        # Validate region
        region = record['region']
        if region not in self.config['valid_regions']:
            errors.append(f"Invalid region: {region}")
        
        # Check for high-value orders
        revenue = price * quantity
        if revenue > self.config['high_value_threshold']:
            warnings.append(f"High-value order: ₹{revenue:,} - Requires approval")
        
        # Validate product name
        product = str(record['product']).strip()
        if len(product) < 2:
            errors.append("Product name too short")
        
        # Validate customer ID format
        customer_id = str(record['customer_id']).strip()
        if not customer_id.startswith('C') or len(customer_id) < 4:
            errors.append(f"Invalid customer ID format: {customer_id}")
        
        is_valid = len(errors) == 0
        return is_valid, errors, warnings
    
    def validate_dataframe(self, df):
        """
        Validate entire dataframe
        
        Args:
            df (pd.DataFrame): Dataframe to validate
            
        Returns:
            tuple: (valid_df, invalid_df, report)
        """
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}🔍 DATA VALIDATION PIPELINE STARTED")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        print(f"{Fore.YELLOW}📂 Loading data...")
        print(f"   Total records: {len(df)}")
        print(f"   Columns: {', '.join(df.columns)}\n")
        
        valid_records = []
        invalid_records = []
        
        # Process each record
        for idx, row in df.iterrows():
            record_num = idx + 1
            self.validation_results['total_records'] += 1
            
            # Show progress every 1000 records
            if record_num % 1000 == 0:
                print(f"{Fore.BLUE}   Processing record {record_num:,}...")
            
            is_valid, errors, warnings = self.validate_record(row.to_dict(), record_num)
            
            if is_valid:
                self.validation_results['valid_records'] += 1
                valid_records.append(row.to_dict())
                
                # Log warnings
                if warnings:
                    for warning in warnings:
                        self.validation_results['warnings'].append({
                            'record_num': record_num,
                            'warning': warning
                        })
            else:
                self.validation_results['invalid_records'] += 1
                invalid_record = row.to_dict()
                invalid_record['record_num'] = record_num
                invalid_record['errors'] = errors
                invalid_records.append(invalid_record)
                
                # Log errors
                for error in errors:
                    self.validation_results['errors'].append({
                        'record_num': record_num,
                        'error': error
                    })
        
        # Create dataframes
        valid_df = pd.DataFrame(valid_records) if valid_records else pd.DataFrame()
        invalid_df = pd.DataFrame(invalid_records) if invalid_records else pd.DataFrame()
        
        # Generate report
        self.print_report()
        
        return valid_df, invalid_df, self.validation_results
    
    def print_report(self):
        """Print validation report"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}📊 VALIDATION REPORT")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        total = self.validation_results['total_records']
        valid = self.validation_results['valid_records']
        invalid = self.validation_results['invalid_records']
        
        valid_pct = (valid / total * 100) if total > 0 else 0
        invalid_pct = (invalid / total * 100) if total > 0 else 0
        
        print(f"{Fore.WHITE}Total Records:   {total:,}")
        print(f"{Fore.GREEN}✅ Valid:        {valid:,} ({valid_pct:.1f}%)")
        print(f"{Fore.RED}❌ Invalid:      {invalid:,} ({invalid_pct:.1f}%)")
        print(f"{Fore.YELLOW}⚠️  Warnings:     {len(self.validation_results['warnings']):,}\n")
        
        # Show sample errors
        if self.validation_results['errors']:
            print(f"{Fore.RED}Sample Errors (first 5):")
            for error_info in self.validation_results['errors'][:5]:
                print(f"  Record #{error_info['record_num']}: {error_info['error']}")
            
            if len(self.validation_results['errors']) > 5:
                remaining = len(self.validation_results['errors']) - 5
                print(f"  ... and {remaining} more errors\n")
        
        # Show sample warnings
        if self.validation_results['warnings']:
            print(f"{Fore.YELLOW}Sample Warnings (first 5):")
            for warning_info in self.validation_results['warnings'][:5]:
                print(f"  Record #{warning_info['record_num']}: {warning_info['warning']}")
            
            if len(self.validation_results['warnings']) > 5:
                remaining = len(self.validation_results['warnings']) - 5
                print(f"  ... and {remaining} more warnings\n")
        
        print(f"{Fore.CYAN}{'='*70}\n")
    
    def save_results(self, valid_df, invalid_df, output_dir='output'):
        """
        Save validation results to files
        
        Args:
            valid_df (pd.DataFrame): Valid records
            invalid_df (pd.DataFrame): Invalid records
            output_dir (str): Output directory
        """
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save valid records
        if not valid_df.empty:
            valid_file = f"{output_dir}/valid_records_{timestamp}.csv"
            valid_df.to_csv(valid_file, index=False)
            print(f"{Fore.GREEN}✅ Valid records saved: {valid_file}")
        
        # Save invalid records
        if not invalid_df.empty:
            invalid_file = f"{output_dir}/invalid_records_{timestamp}.csv"
            invalid_df.to_csv(invalid_file, index=False)
            print(f"{Fore.RED}❌ Invalid records saved: {invalid_file}")
        
        # Save summary report
        report_file = f"{output_dir}/validation_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("DATA VALIDATION REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Records: {self.validation_results['total_records']:,}\n")
            f.write(f"Valid Records: {self.validation_results['valid_records']:,}\n")
            f.write(f"Invalid Records: {self.validation_results['invalid_records']:,}\n")
            f.write(f"Warnings: {len(self.validation_results['warnings']):,}\n\n")

            if self.validation_results['errors']:
                f.write("ERRORS:\n")
                for error_info in self.validation_results['errors']:
                    f.write(f"  Record #{error_info['record_num']}: {error_info['error']}\n")
        
        
        print(f"{Fore.BLUE}📄 Report saved: {report_file}\n")


def create_test_data():
    """Create test dataset with various validation scenarios"""
    data = {
        'product': [
            'Laptop', 'Mouse', '', 'Monitor', 'Keyboard',
            'Headphones', 'Webcam', 'Speaker', 'Tablet', 'Phone'
        ],
        'price': [
            75000, -500, 1500, 25000, 1500,
            2000, 3500, 5000, 45000, 1200000  # Last one exceeds max
        ],
        'quantity': [
            2, 5, 0, 1, 3,
            4, 2, 15000, 1, 2  # 15000 exceeds max
        ],
        'customer_id': [
            'C001', 'C002', 'C003', 'INVALID', 'C005',
            'C006', 'C007', 'C008', 'C009', 'C010'
        ],
        'region': [
            'West', 'East', 'North', 'South', 'InvalidRegion',
            'West', 'East', 'North', 'South', 'West'
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_csv('test_sales_data.csv', index=False)
    return df


def main():
    """Main execution function"""
    print(f"\n{Fore.MAGENTA}{'='*70}")
    print(f"{Fore.MAGENTA}🚀 PRODUCTION DATA VALIDATION PIPELINE")
    print(f"{Fore.MAGENTA}{'='*70}\n")
    
    # Create test data
    print(f"{Fore.YELLOW}📝 Creating test dataset...")
    df = create_test_data()
    print(f"{Fore.GREEN}✅ Test data created: test_sales_data.csv\n")
    
    # Initialize validator
    validator = DataValidator()
    
    # Run validation
    valid_df, invalid_df, results = validator.validate_dataframe(df)
    
    # Save results
    validator.save_results(valid_df, invalid_df)
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"{Fore.GREEN}✅ VALIDATION PIPELINE COMPLETED")
    print(f"{Fore.GREEN}{'='*70}\n")


if __name__ == "__main__":
    main()