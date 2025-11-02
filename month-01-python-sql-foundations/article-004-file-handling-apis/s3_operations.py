# s3_operations.py - AWS S3 Operations

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class S3Manager:
    """Manage AWS S3 operations"""
    
    def __init__(self):
        """Initialize S3 client"""
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'ap-south-1')
            )
            
            self.bucket_name = os.getenv('S3_BUCKET_NAME')
            
            print(f"✅ S3 client initialized")
            print(f"   Region: {os.getenv('AWS_REGION', 'ap-south-1')}")
            print(f"   Bucket: {self.bucket_name}\n")
            
        except NoCredentialsError:
            print("❌ AWS credentials not found!")
            print("   Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
            self.s3_client = None
    
    def list_buckets(self):
        """List all S3 buckets"""
        try:
            print("📦 Listing S3 buckets...")
            
            response = self.s3_client.list_buckets()
            buckets = response.get('Buckets', [])
            
            print(f"✅ Found {len(buckets)} buckets:\n")
            for bucket in buckets:
                print(f"   - {bucket['Name']} (Created: {bucket['CreationDate']})")
            print()
            
            return buckets
            
        except Exception as e:
            print(f"❌ Error listing buckets: {e}")
            return []
    
    def create_bucket(self, bucket_name=None):
        """Create S3 bucket"""
        bucket_name = bucket_name or self.bucket_name
        
        try:
            print(f"🪣 Creating bucket: {bucket_name}")
            
            # For regions other than us-east-1, need LocationConstraint
            region = os.getenv('AWS_REGION', 'ap-south-1')
            
            if region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            
            print(f"✅ Bucket created successfully\n")
            return True
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print(f"ℹ️  Bucket already exists and is owned by you\n")
                return True
            else:
                print(f"❌ Error creating bucket: {e}")
                return False
    
    def upload_file(self, local_path, s3_key=None):
        """
        Upload file to S3
        
        Args:
            local_path (str): Local file path
            s3_key (str): S3 object key (path in bucket)
        """
        if not s3_key:
            s3_key = os.path.basename(local_path)
        
        try:
            print(f"⬆️  Uploading: {local_path} → s3://{self.bucket_name}/{s3_key}")
            
            # Get file size
            file_size = os.path.getsize(local_path) / 1024  # KB
            
            self.s3_client.upload_file(local_path, self.bucket_name, s3_key)
            
            print(f"✅ Uploaded successfully ({file_size:.2f} KB)\n")
            return True
            
        except FileNotFoundError:
            print(f"❌ File not found: {local_path}")
            return False
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return False
    
    def download_file(self, s3_key, local_path):
        """
        Download file from S3
        
        Args:
            s3_key (str): S3 object key
            local_path (str): Local file path to save
        """
        try:
            print(f"⬇️  Downloading: s3://{self.bucket_name}/{s3_key} → {local_path}")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(local_path) or '.', exist_ok=True)
            
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            
            file_size = os.path.getsize(local_path) / 1024  # KB
            print(f"✅ Downloaded successfully ({file_size:.2f} KB)\n")
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def list_objects(self, prefix=''):
        """
        List objects in bucket
        
        Args:
            prefix (str): Filter by prefix (folder path)
        """
        try:
            print(f"📋 Listing objects in: s3://{self.bucket_name}/{prefix}")
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            objects = response.get('Contents', [])
            
            print(f"✅ Found {len(objects)} objects:\n")
            
            for obj in objects:
                size_kb = obj['Size'] / 1024
                print(f"   - {obj['Key']} ({size_kb:.2f} KB)")
            print()
            
            return objects
            
        except Exception as e:
            print(f"❌ Error listing objects: {e}")
            return []
    
    def delete_object(self, s3_key):
        """Delete object from S3"""
        try:
            print(f"🗑️  Deleting: s3://{self.bucket_name}/{s3_key}")
            
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            
            print(f"✅ Deleted successfully\n")
            return True
            
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False
    
    def upload_dataframe(self, df, s3_key, format='parquet'):
        """
        Upload DataFrame to S3
        
        Args:
            df (pd.DataFrame): DataFrame to upload
            s3_key (str): S3 object key
            format (str): File format ('parquet', 'csv', 'json')
        """
        try:
            print(f"⬆️  Uploading DataFrame to: s3://{self.bucket_name}/{s3_key}")
            print(f"   Format: {format}")
            print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Save to temporary file
            temp_file = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            
            if format == 'parquet':
                df.to_parquet(temp_file, index=False)
            elif format == 'csv':
                df.to_csv(temp_file, index=False)
            elif format == 'json':
                df.to_json(temp_file, orient='records', indent=2)
            else:
                print(f"❌ Unsupported format: {format}")
                return False
            
            # Upload to S3
            success = self.upload_file(temp_file, s3_key)
            
            # Clean up temp file
            os.remove(temp_file)
            
            return success
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return False
    
    def read_dataframe(self, s3_key, format='parquet'):
        """
        Read DataFrame from S3
        
        Args:
            s3_key (str): S3 object key
            format (str): File format ('parquet', 'csv', 'json')
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            print(f"⬇️  Reading DataFrame from: s3://{self.bucket_name}/{s3_key}")
            
            # Download to temporary file
            temp_file = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            
            if not self.download_file(s3_key, temp_file):
                return None
            
            # Read based on format
            if format == 'parquet':
                df = pd.read_parquet(temp_file)
            elif format == 'csv':
                df = pd.read_csv(temp_file)
            elif format == 'json':
                df = pd.read_json(temp_file)
            else:
                print(f"❌ Unsupported format: {format}")
                return None
            
            # Clean up temp file
            os.remove(temp_file)
            
            print(f"✅ Loaded DataFrame: {df.shape[0]} rows × {df.shape[1]} columns\n")
            return df
            
        except Exception as e:
            print(f"❌ Read failed: {e}")
            return None


def demonstrate_s3_operations():
    """Demonstrate S3 operations"""
    
    print("="*70)
    print("☁️  AWS S3 OPERATIONS DEMONSTRATION")
    print("="*70 + "\n")
    
    # Check if credentials are set
    if not os.getenv('AWS_ACCESS_KEY_ID'):
        print("⚠️  AWS credentials not found in .env file")
        print("\nTo use S3 operations:")
        print("1. Create .env file in project root")
        print("2. Add your AWS credentials:")
        print("   AWS_ACCESS_KEY_ID=your_key")
        print("   AWS_SECRET_ACCESS_KEY=your_secret")
        print("   AWS_REGION=ap-south-1")
        print("   S3_BUCKET_NAME=your-bucket-name")
        print("\n⚠️  Skipping S3 demonstration\n")
        return
    
    s3 = S3Manager()
    
    if not s3.s3_client:
        return
    
    # List buckets
    s3.list_buckets()
    
    # Create sample data
    print("📝 Creating sample data...")
    sample_data = pd.DataFrame({
        'date': pd.date_range('2025-01-01', periods=10),
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'] * 2,
        'revenue': [150000, 5000, 7500, 25000, 8000] * 2,
        'region': ['West', 'East', 'North', 'South', 'West'] * 2
    })
    print(f"✅ Created sample data: {len(sample_data)} rows\n")
    
    # Upload DataFrame as Parquet
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    s3_key = f"data/sales/sales_{timestamp}.parquet"
    
    s3.upload_dataframe(sample_data, s3_key, format='parquet')
    
    # List objects
    s3.list_objects(prefix='data/')
    
    # Download and read
    df_downloaded = s3.read_dataframe(s3_key, format='parquet')
    if df_downloaded is not None:
        print("Downloaded data:")
        print(df_downloaded.head())
        print()


if __name__ == "__main__":
    demonstrate_s3_operations()
    
    print("="*70)
    print("✅ S3 OPERATIONS COMPLETE")
    print("="*70)