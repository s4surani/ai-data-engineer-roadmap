# multi_source_pipeline.py - Multi-Source Data Ingestion Pipeline

import pandas as pd
from datetime import datetime
import os
import json
from colorama import Fore, Style, init

# Import our modules
from api_client import APIClient
from database_operations import DatabaseManager
from s3_operations import S3Manager

# Initialize colorama
init(autoreset=True)


class DataPipeline:
    """Multi-source data ingestion pipeline"""
    
    def __init__(self, config):
        """
        Initialize pipeline
        
        Args:
            config (dict): Pipeline configuration
        """
        self.config = config
        self.data_sources = {}
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'sources': {},
            'errors': []
        }
    
    def log(self, message, level='INFO'):
        """Log pipeline messages"""
        colors = {
            'INFO': Fore.CYAN,
            'SUCCESS': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED
        }
        
        color = colors.get(level, Fore.WHITE)
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{color}[{timestamp}] [{level}] {message}{Style.RESET_ALL}")
    
    def fetch_api_data(self):
        """Fetch data from REST APIs"""
        self.log("Fetching data from APIs...", 'INFO')
        
        try:
            # Fetch cryptocurrency prices
            api_client = APIClient('https://api.coingecko.com/api/v3')
            
            crypto_data = api_client.get(
                'simple/price',
                params={
                    'ids': 'bitcoin,ethereum',
                    'vs_currencies': 'usd,inr'
                }
            )
            
            # Convert to DataFrame
            df_crypto = pd.DataFrame([
                {
                    'cryptocurrency': crypto,
                    'usd_price': data['usd'],
                    'inr_price': data['inr'],
                    'timestamp': datetime.now()
                }
                for crypto, data in crypto_data.items()
            ])
            
            self.data_sources['api_crypto'] = df_crypto
            self.results['sources']['api'] = {
                'status': 'success',
                'records': len(df_crypto)
            }
            
            self.log(f"✅ Fetched {len(df_crypto)} crypto prices", 'SUCCESS')
            return df_crypto
            
        except Exception as e:
            self.log(f"❌ API fetch failed: {e}", 'ERROR')
            self.results['sources']['api'] = {
                'status': 'failed',
                'error': str(e)
            }
            return None
    
    def fetch_database_data(self):
        """Fetch data from database"""
        self.log("Fetching data from database...", 'INFO')
        
        try:
            db_config = self.config.get('database', {})
            db = DatabaseManager(db_config)
            
            if not db.connect():
                raise Exception("Database connection failed")
            
            # Fetch orders data
            query = """
            SELECT 
                o.order_id,
                c.name as customer_name,
                p.name as product_name,
                o.quantity,
                p.price,
                (o.quantity * p.price) as revenue,
                o.order_date,
                o.region
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN products p ON o.product_id = p.product_id
            WHERE o.status = 'Delivered'
            """
            
            df_orders = pd.read_sql(query, db.engine)
            
            db.disconnect()
            
            self.data_sources['database_orders'] = df_orders
            self.results['sources']['database'] = {
                'status': 'success',
                'records': len(df_orders)
            }
            
            self.log(f"✅ Fetched {len(df_orders)} orders from database", 'SUCCESS')
            return df_orders
            
        except Exception as e:
            self.log(f"❌ Database fetch failed: {e}", 'ERROR')
            self.results['sources']['database'] = {
                'status': 'failed',
                'error': str(e)
            }
            return None
    
    def read_file_data(self):
        """Read data from local files"""
        self.log("Reading data from files...", 'INFO')
        
        try:
            # Read CSV
            if os.path.exists('sample_sales.csv'):
                df_csv = pd.read_csv('sample_sales.csv')
                self.data_sources['file_csv'] = df_csv
                self.log(f"✅ Read {len(df_csv)} rows from CSV", 'SUCCESS')
            
            # Read JSON
            if os.path.exists('products.json'):
                df_json = pd.read_json('products.json')
                self.data_sources['file_json'] = df_json
                self.log(f"✅ Read {len(df_json)} rows from JSON", 'SUCCESS')
            
            # Read Excel
            if os.path.exists('sample_sales.xlsx'):
                df_excel = pd.read_excel('sample_sales.xlsx', engine='openpyxl')
                self.data_sources['file_excel'] = df_excel
                self.log(f"✅ Read {len(df_excel)} rows from Excel", 'SUCCESS')
            
            self.results['sources']['files'] = {
                'status': 'success',
                'sources': list(self.data_sources.keys())
            }
            
            return True
            
        except Exception as e:
            self.log(f"❌ File read failed: {e}", 'ERROR')
            self.results['sources']['files'] = {
                'status': 'failed',
                'error': str(e)
            }
            return False
    
    def transform_data(self):
        """Transform and combine data"""
        self.log("Transforming data...", 'INFO')
        
        try:
            # Combine all data sources
            combined_data = {}
            
            for source_name, df in self.data_sources.items():
                # Add source column
                df_copy = df.copy()
                df_copy['data_source'] = source_name
                df_copy['ingestion_timestamp'] = datetime.now()
                
                combined_data[source_name] = df_copy
            
            self.log(f"✅ Transformed {len(combined_data)} data sources", 'SUCCESS')
            return combined_data
            
        except Exception as e:
            self.log(f"❌ Transformation failed: {e}", 'ERROR')
            return None
    
    def save_to_s3(self, data):
        """Save data to S3"""
        self.log("Saving data to S3...", 'INFO')
        
        try:
            s3 = S3Manager()
            
            if not s3.s3_client:
                self.log("⚠️  S3 client not available, skipping upload", 'WARNING')
                return False
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            for source_name, df in data.items():
                s3_key = f"pipeline_output/{source_name}_{timestamp}.parquet"
                
                if s3.upload_dataframe(df, s3_key, format='parquet'):
                    self.log(f"✅ Uploaded {source_name} to S3", 'SUCCESS')
                else:
                    self.log(f"⚠️  Failed to upload {source_name}", 'WARNING')
            
            self.results['s3_upload'] = {
                'status': 'success',
                'timestamp': timestamp
            }
            
            return True
            
        except Exception as e:
            self.log(f"❌ S3 upload failed: {e}", 'ERROR')
            self.results['s3_upload'] = {
                'status': 'failed',
                'error': str(e)
            }
            return False
    
    def save_locally(self, data):
        """Save data to local files"""
        self.log("Saving data locally...", 'INFO')
        
        try:
            output_dir = 'output/pipeline_results'
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            for source_name, df in data.items():
                # Save as Parquet
                parquet_file = f"{output_dir}/{source_name}_{timestamp}.parquet"
                df.to_parquet(parquet_file, index=False)
                
                # Save as CSV for easy viewing
                csv_file = f"{output_dir}/{source_name}_{timestamp}.csv"
                df.to_csv(csv_file, index=False)
                
                self.log(f"✅ Saved {source_name} locally", 'SUCCESS')
            
            # Save pipeline results
            results_file = f"{output_dir}/pipeline_results_{timestamp}.json"
            with open(results_file, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            self.log(f"✅ Saved pipeline results to {results_file}", 'SUCCESS')
            
            return True
            
        except Exception as e:
            self.log(f"❌ Local save failed: {e}", 'ERROR')
            return False
    
    def run(self):
        """Execute the complete pipeline"""
        self.log("="*70, 'INFO')
        self.log("🚀 STARTING MULTI-SOURCE DATA PIPELINE", 'INFO')
        self.log("="*70, 'INFO')
        
        start_time = datetime.now()
        
        # Step 1: Fetch from APIs
        self.fetch_api_data()
        
        # Step 2: Fetch from database
        self.fetch_database_data()
        
        # Step 3: Read from files
        self.read_file_data()
        
        # Step 4: Transform data
        transformed_data = self.transform_data()
        
        if transformed_data:
            # Step 5: Save to S3
            self.save_to_s3(transformed_data)
            
            # Step 6: Save locally
            self.save_locally(transformed_data)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        
        self.log("="*70, 'INFO')
        self.log(f"✅ PIPELINE COMPLETED in {duration:.2f} seconds", 'SUCCESS')
        self.log("="*70, 'INFO')
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print pipeline execution summary"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}📊 PIPELINE EXECUTION SUMMARY")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"\nData Sources:")
        
        for source, info in self.results['sources'].items():
            status = info.get('status', 'unknown')
            color = Fore.GREEN if status == 'success' else Fore.RED
            
            print(f"  {color}• {source}: {status}{Style.RESET_ALL}")
            
            if status == 'success' and 'records' in info:
                print(f"    Records: {info['records']}")
            elif status == 'failed':
                print(f"    Error: {info.get('error', 'Unknown')}")
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    # Pipeline configuration
    config = {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'database': 'sales_db',
            'user': 'postgres',
            'password': 'postgres'
        }
    }
    
    # Create and run pipeline
    pipeline = DataPipeline(config)
    pipeline.run()