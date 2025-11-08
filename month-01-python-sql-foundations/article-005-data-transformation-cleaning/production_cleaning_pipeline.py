# production_cleaning_pipeline.py - Complete Production Data Cleaning Pipeline

import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
from colorama import Fore, Style, init

init(autoreset=True)


class DataCleaningPipeline:
    """Production-grade data cleaning pipeline"""
    
    def __init__(self, config=None):
        """
        Initialize cleaning pipeline
        
        Args:
            config (dict): Pipeline configuration
        """
        self.config = config or self.get_default_config()
        self.cleaning_report = {
            'timestamp': datetime.now().isoformat(),
            'steps': [],
            'statistics': {}
        }
    
    @staticmethod
    def get_default_config():
        """Get default pipeline configuration"""
        return {
            'missing_values': {
                'numeric_strategy': 'median',
                'categorical_strategy': 'mode',
                'drop_threshold': 0.5
            },
            'duplicates': {
                'subset': None,
                'keep': 'first'
            },
            'outliers': {
                'method': 'iqr',
                'threshold': 1.5
            },
            'data_types': {
                'auto_convert': True
            },
            'text_cleaning': {
                'lowercase_emails': True,
                'standardize_phones': True,
                'title_case_names': True
            }
        }
    
    def log_step(self, step_name, details):
        """Log pipeline step"""
        self.cleaning_report['steps'].append({
            'step': step_name,
            'timestamp': datetime.now().isoformat(),
            'details': details
        })
    
    def analyze_data_quality(self, df):
        """Analyze initial data quality"""
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"🔍 ANALYZING DATA QUALITY")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        stats = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
            'duplicate_rows': df.duplicated().sum(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
        }
        
        print(f"Dataset Overview:")
        print(f"  Rows: {stats['total_rows']:,}")
        print(f"  Columns: {stats['total_columns']}")
        print(f"  Missing Values: {stats['missing_values']:,} ({stats['missing_percentage']:.2f}%)")
        print(f"  Duplicate Rows: {stats['duplicate_rows']:,}")
        print(f"  Memory Usage: {stats['memory_usage_mb']:.2f} MB")
        print()
        
        self.cleaning_report['statistics']['initial'] = stats
        self.log_step('analyze_quality', stats)
        
        return stats
    
    def handle_missing_values(self, df):
        """Handle missing values based on configuration"""
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"🔧 HANDLING MISSING VALUES")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        df_cleaned = df.copy()
        missing_before = df_cleaned.isnull().sum().sum()
        
        # Handle numeric columns
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        strategy = self.config['missing_values']['numeric_strategy']
        
        for col in numeric_cols:
            missing_count = df_cleaned[col].isnull().sum()
            if missing_count > 0:
                if strategy == 'mean':
                    fill_value = df_cleaned[col].mean()
                elif strategy == 'median':
                    fill_value = df_cleaned[col].median()
                else:
                    fill_value = 0
                
                df_cleaned[col].fillna(fill_value, inplace=True)
                print(f"  ✅ {col}: Filled {missing_count} values with {strategy} ({fill_value:.2f})")
        
        # Handle categorical columns
        categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
        strategy = self.config['missing_values']['categorical_strategy']
        
        for col in categorical_cols:
            missing_count = df_cleaned[col].isnull().sum()
            if missing_count > 0:
                if strategy == 'mode':
                    fill_value = df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else 'Unknown'
                else:
                    fill_value = 'Unknown'
                
                df_cleaned[col].fillna(fill_value, inplace=True)
                print(f"  ✅ {col}: Filled {missing_count} values with {strategy} ('{fill_value}')")
        
        missing_after = df_cleaned.isnull().sum().sum()
        
        print(f"\nMissing values: {missing_before} → {missing_after}")
        print()
        
        self.log_step('handle_missing', {
            'before': missing_before,
            'after': missing_after,
            'filled': missing_before - missing_after
        })
        
        return df_cleaned
    
    def remove_duplicates(self, df):
        """Remove duplicate rows"""
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"🗑️  REMOVING DUPLICATES")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        rows_before = len(df)
        
        subset = self.config['duplicates']['subset']
        keep = self.config['duplicates']['keep']
        
        df_cleaned = df.drop_duplicates(subset=subset, keep=keep)
        
        rows_after = len(df_cleaned)
        duplicates_removed = rows_before - rows_after
        
        print(f"Rows: {rows_before:,} → {rows_after:,}")
        print(f"Duplicates removed: {duplicates_removed:,}")
        print()
        
        self.log_step('remove_duplicates', {
            'before': rows_before,
            'after': rows_after,
            'removed': duplicates_removed
        })
        
        return df_cleaned
    
    def handle_outliers(self, df):
        """Handle outliers in numeric columns"""
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"📊 HANDLING OUTLIERS")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        df_cleaned = df.copy()
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        
        method = self.config['outliers']['method']
        threshold = self.config['outliers']['threshold']
        
        outliers_handled = {}
        
        for col in numeric_cols:
            if method == 'iqr':
                Q1 = df_cleaned[col].quantile(0.25)
                Q3 = df_cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                outliers_count = ((df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)).sum()
                
                if outliers_count > 0:
                    # Cap outliers
                    df_cleaned[col] = df_cleaned[col].clip(lower=lower_bound, upper=upper_bound)
                    outliers_handled[col] = outliers_count
                    print(f"  ✅ {col}: Capped {outliers_count} outliers")
        
        print(f"\nTotal outliers handled: {sum(outliers_handled.values())}")
        print()
        
        self.log_step('handle_outliers', outliers_handled)
        
        return df_cleaned
    
    def clean_text_data(self, df):
        """Clean text columns"""
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"🧼 CLEANING TEXT DATA")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        df_cleaned = df.copy()
        
        # Clean email columns
        email_cols = [col for col in df_cleaned.columns if 'email' in col.lower()]
        if email_cols and self.config['text_cleaning']['lowercase_emails']:
            for col in email_cols:
                df_cleaned[col] = df_cleaned[col].str.lower().str.strip()
                print(f"  ✅ {col}: Lowercased and trimmed")
        
        # Clean name columns
        name_cols = [col for col in df_cleaned.columns if 'name' in col.lower()]
        if name_cols and self.config['text_cleaning']['title_case_names']:
            for col in name_cols:
                df_cleaned[col] = df_cleaned[col].str.strip().str.title()
                print(f"  ✅ {col}: Title cased and trimmed")
        
        # Clean phone columns
        phone_cols = [col for col in df_cleaned.columns if 'phone' in col.lower()]
        if phone_cols and self.config['text_cleaning']['standardize_phones']:
            for col in phone_cols:
                df_cleaned[col] = df_cleaned[col].astype(str).str.replace(r'\D', '', regex=True)
                print(f"  ✅ {col}: Standardized format")
        
        print()
        
        self.log_step('clean_text', {
            'email_cols': email_cols,
            'name_cols': name_cols,
            'phone_cols': phone_cols
        })
        
        return df_cleaned
    
    def optimize_data_types(self, df):
        """Optimize data types for memory efficiency"""
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"⚡ OPTIMIZING DATA TYPES")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        df_optimized = df.copy()
        memory_before = df_optimized.memory_usage(deep=True).sum() / 1024**2
        
        # Optimize integers
        for col in df_optimized.select_dtypes(include=['int64']).columns:
            df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
        
        # Optimize floats
        for col in df_optimized.select_dtypes(include=['float64']).columns:
            df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
        
        # Convert to category
        for col in df_optimized.select_dtypes(include=['object']).columns:
            num_unique = df_optimized[col].nunique()
            num_total = len(df_optimized[col])
            if num_unique / num_total < 0.5:
                df_optimized[col] = df_optimized[col].astype('category')
        
        memory_after = df_optimized.memory_usage(deep=True).sum() / 1024**2
        savings = ((memory_before - memory_after) / memory_before) * 100
        
        print(f"Memory usage: {memory_before:.2f} MB → {memory_after:.2f} MB")
        print(f"Memory saved: {savings:.1f}%")
        print()
        
        self.log_step('optimize_types', {
            'memory_before_mb': memory_before,
            'memory_after_mb': memory_after,
            'savings_percent': savings
        })
        
        return df_optimized
    
    def generate_report(self, df_original, df_cleaned):
        """Generate cleaning report"""
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"📊 CLEANING REPORT")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        # Final statistics
        final_stats = {
            'total_rows': len(df_cleaned),
            'total_columns': len(df_cleaned.columns),
            'missing_values': df_cleaned.isnull().sum().sum(),
            'duplicate_rows': df_cleaned.duplicated().sum(),
            'memory_usage_mb': df_cleaned.memory_usage(deep=True).sum() / 1024**2
        }
        
        self.cleaning_report['statistics']['final'] = final_stats
        
        # Print summary
        print("Before → After:")
        print(f"  Rows: {self.cleaning_report['statistics']['initial']['total_rows']:,} → {final_stats['total_rows']:,}")
        print(f"  Missing Values: {self.cleaning_report['statistics']['initial']['missing_values']:,} → {final_stats['missing_values']:,}")
        print(f"  Duplicates: {self.cleaning_report['statistics']['initial']['duplicate_rows']:,} → {final_stats['duplicate_rows']:,}")
        print(f"  Memory: {self.cleaning_report['statistics']['initial']['memory_usage_mb']:.2f} MB → {final_stats['memory_usage_mb']:.2f} MB")
        print()
        
        print("Pipeline Steps:")
        for i, step in enumerate(self.cleaning_report['steps'], 1):
            print(f"  {i}. {step['step']}")
        print()
        
        return self.cleaning_report
    
    def run(self, df):
        """Execute complete cleaning pipeline"""
        
        print(f"{Fore.MAGENTA}{'='*70}")
        print(f"🚀 STARTING DATA CLEANING PIPELINE")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        start_time = datetime.now()
        
        # Step 1: Analyze quality
        self.analyze_data_quality(df)
        
        # Step 2: Handle missing values
        df = self.handle_missing_values(df)
        
        # Step 3: Remove duplicates
        df = self.remove_duplicates(df)
        
        # Step 4: Handle outliers
        df = self.handle_outliers(df)
        
        # Step 5: Clean text data
        df = self.clean_text_data(df)
        
        # Step 6: Optimize data types
        df = self.optimize_data_types(df)
        
        # Generate report
        report = self.generate_report(df, df)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"{Fore.GREEN}{'='*70}")
        print(f"✅ PIPELINE COMPLETED in {duration:.2f} seconds")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        return df, report


def create_messy_production_dataset():
    """Create a realistic messy dataset"""
    
    np.random.seed(42)
    
    # Create base data
    n_rows = 1000
    
    data = {
        'customer_id': [f'C{i:04d}' for i in range(1, n_rows + 1)],
        'name': np.random.choice(['mayurkumar surani', 'RAHUL SHARMA', 'Priya  Patel', 
                                  'amit kumar', 'Sneha Desai', None], n_rows),
        'email': np.random.choice(['MAYUR@EXAMPLE.COM', 'rahul@example.com', 
                                   'priya@example.com', None, ''], n_rows),
        'phone': np.random.choice(['9876543210', '+91-8765432109', '7654321098', None], n_rows),
        'age': np.random.choice(list(range(20, 60)) + [None, 150, 200], n_rows),
        'salary': np.random.choice(list(range(500000, 2000000, 100000)) + [None, 10000000], n_rows),
        'purchase_amount': np.random.choice(list(range(10000, 100000, 5000)) + [None, 500000], n_rows),
        'city': np.random.choice(['Pune', 'Mumbai', 'Bangalore', 'Delhi', None], n_rows),
        'purchase_date': pd.date_range('2024-01-01', periods=n_rows, freq='H')
    }
    
    df = pd.DataFrame(data)
    
    # Add duplicates
    df = pd.concat([df, df.sample(50)], ignore_index=True)
    
    df.to_csv('messy_production_data.csv', index=False)
    print(f"{Fore.GREEN}✅ Created messy production dataset: messy_production_data.csv{Style.RESET_ALL}\n")
    
    return df


if __name__ == "__main__":
    # Create messy dataset
    df_messy = create_messy_production_dataset()
    
    # Initialize pipeline
    pipeline = DataCleaningPipeline()
    
    # Run pipeline
    df_cleaned, report = pipeline.run(df_messy)
    
    # Save results
    os.makedirs('output', exist_ok=True)
    df_cleaned.to_csv('output/cleaned_production_data.csv', index=False)
    df_cleaned.to_parquet('output/cleaned_production_data.parquet', index=False)
    
    # Save report
    with open('output/cleaning_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"{Fore.GREEN}💾 Saved cleaned data and report to output/ directory{Style.RESET_ALL}")