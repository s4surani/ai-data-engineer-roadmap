# json_operations.py - JSON File Operations

import json
import pandas as pd
from datetime import datetime
import os


def read_json_basic(file_path):
    """
    Read JSON file (basic Python)
    
    Args:
        file_path (str): Path to JSON file
        
    Returns:
        dict/list: Parsed JSON data
    """
    try:
        print(f"📂 Reading JSON: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded JSON data")
        print(f"   Type: {type(data).__name__}")
        
        if isinstance(data, list):
            print(f"   Records: {len(data)}")
        elif isinstance(data, dict):
            print(f"   Keys: {', '.join(data.keys())}")
        
        print()
        return data
        
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def write_json_basic(data, file_path, indent=2):
    """
    Write data to JSON file
    
    Args:
        data (dict/list): Data to write
        file_path (str): Output file path
        indent (int): Indentation spaces
    """
    try:
        print(f"💾 Writing JSON: {file_path}")
        
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        file_size = os.path.getsize(file_path) / 1024
        print(f"✅ Saved JSON ({file_size:.2f} KB)\n")
        
    except Exception as e:
        print(f"❌ Error writing JSON: {e}")


def read_json_pandas(file_path):
    """
    Read JSON file using pandas
    
    Args:
        file_path (str): Path to JSON file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    try:
        print(f"📂 Reading JSON with pandas: {file_path}")
        
        df = pd.read_json(file_path)
        
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"   Columns: {', '.join(df.columns)}\n")
        
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def json_to_dataframe(json_data):
    """
    Convert JSON data to DataFrame
    
    Args:
        json_data (dict/list): JSON data
        
    Returns:
        pd.DataFrame: Converted data
    """
    try:
        print("🔄 Converting JSON to DataFrame...")
        
        if isinstance(json_data, list):
            df = pd.DataFrame(json_data)
        elif isinstance(json_data, dict):
            df = pd.DataFrame([json_data])
        else:
            print("❌ Error: Unsupported JSON structure")
            return None
        
        print(f"✅ Created DataFrame: {df.shape[0]} rows × {df.shape[1]} columns\n")
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def read_jsonl(file_path):
    """
    Read JSON Lines file (one JSON object per line)
    
    Args:
        file_path (str): Path to JSONL file
        
    Returns:
        list: List of JSON objects
    """
    try:
        print(f"📂 Reading JSON Lines: {file_path}")
        
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    obj = json.loads(line.strip())
                    data.append(obj)
                except json.JSONDecodeError:
                    print(f"⚠️  Warning: Invalid JSON on line {line_num}")
        
        print(f"✅ Loaded {len(data)} records\n")
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def write_jsonl(data, file_path):
    """
    Write data as JSON Lines
    
    Args:
        data (list): List of dictionaries
        file_path (str): Output file path
    """
    try:
        print(f"💾 Writing JSON Lines: {file_path}")
        
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for obj in data:
                f.write(json.dumps(obj, ensure_ascii=False) + '\n')
        
        print(f"✅ Saved {len(data)} records\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def create_sample_json():
    """Create sample JSON files for testing"""
    
    # Sample 1: Simple JSON object
    config = {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'sales_db',
            'user': 'admin'
        },
        'api': {
            'base_url': 'https://api.example.com',
            'timeout': 30,
            'retry_attempts': 3
        },
        'features': {
            'enable_caching': True,
            'enable_logging': True,
            'log_level': 'INFO'
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ Created: config.json")
    
    # Sample 2: JSON array
    products = [
        {
            'id': 1,
            'name': 'Laptop',
            'price': 75000,
            'category': 'Electronics',
            'in_stock': True,
            'tags': ['computer', 'portable', 'work']
        },
        {
            'id': 2,
            'name': 'Mouse',
            'price': 500,
            'category': 'Electronics',
            'in_stock': True,
            'tags': ['computer', 'accessory']
        },
        {
            'id': 3,
            'name': 'Keyboard',
            'price': 1500,
            'category': 'Electronics',
            'in_stock': False,
            'tags': ['computer', 'accessory', 'mechanical']
        }
    ]
    
    with open('products.json', 'w') as f:
        json.dump(products, f, indent=2)
    print("✅ Created: products.json")
    
    # Sample 3: JSON Lines
    events = [
        {'timestamp': '2025-01-01T10:00:00', 'event': 'login', 'user_id': 'U001'},
        {'timestamp': '2025-01-01T10:05:00', 'event': 'purchase', 'user_id': 'U001', 'amount': 1500},
        {'timestamp': '2025-01-01T10:10:00', 'event': 'logout', 'user_id': 'U001'}
    ]
    
    with open('events.jsonl', 'w') as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
    print("✅ Created: events.jsonl\n")


if __name__ == "__main__":
    print("="*70)
    print("📊 JSON OPERATIONS DEMONSTRATION")
    print("="*70 + "\n")
    
    # Create sample files
    create_sample_json()
    
    # Read JSON object
    print("1. Read JSON Object:")
    config = read_json_basic('config.json')
    if config:
        print(f"   Database host: {config['database']['host']}")
        print(f"   API URL: {config['api']['base_url']}")
    print()
    
    # Read JSON array
    print("2. Read JSON Array:")
    products = read_json_basic('products.json')
    if products:
        print(f"   First product: {products[0]['name']}")
    print()
    
    # Convert to DataFrame
    print("3. Convert JSON to DataFrame:")
    if products:
        df = json_to_dataframe(products)
        if df is not None:
            print(df)
    print()
    
    # Read JSON Lines
    print("4. Read JSON Lines:")
    events = read_jsonl('events.jsonl')
    if events:
        print(f"   Total events: {len(events)}")
        print(f"   First event: {events[0]}")
    print()
    
    # Write JSON
    print("5. Write JSON:")
    summary = {
        'total_products': len(products) if products else 0,
        'total_events': len(events) if events else 0,
        'generated_at': datetime.now().isoformat()
    }
    write_json_basic(summary, 'output/summary.json')
    
    print("="*70)
    print("✅ JSON OPERATIONS COMPLETE")
    print("="*70)