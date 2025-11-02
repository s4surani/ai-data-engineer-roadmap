# database_operations.py - Database Operations

import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2
from datetime import datetime
import os


class DatabaseManager:
    """Manage database connections and operations"""
    
    def __init__(self, db_config):
        """
        Initialize database manager
        
        Args:
            db_config (dict): Database configuration
        """
        self.config = db_config
        self.engine = None
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            print(f"🔌 Connecting to database: {self.config['database']}")
            
            # Create SQLAlchemy engine
            connection_string = (
                f"postgresql://{self.config['user']}:{self.config['password']}"
                f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
            )
            
            self.engine = create_engine(connection_string)
            self.connection = self.engine.connect()
            
            print(f"✅ Connected successfully\n")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("🔌 Disconnected from database\n")
    
    def execute_query(self, query, params=None):
        """
        Execute SQL query
        
        Args:
            query (str): SQL query
            params (dict): Query parameters
            
        Returns:
            list: Query results
        """
        try:
            print(f"📝 Executing query...")
            
            if params:
                result = self.connection.execute(text(query), params)
            else:
                result = self.connection.execute(text(query))
            
            # Fetch results if it's a SELECT query
            if query.strip().upper().startswith('SELECT'):
                rows = result.fetchall()
                print(f"✅ Retrieved {len(rows)} rows\n")
                return rows
            else:
                self.connection.commit()
                print(f"✅ Query executed successfully\n")
                return []
                
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return []
    
    def read_table(self, table_name, limit=None):
        """
        Read entire table into DataFrame
        
        Args:
            table_name (str): Table name
            limit (int): Maximum rows to fetch
            
        Returns:
            pd.DataFrame: Table data
        """
        try:
            print(f"📊 Reading table: {table_name}")
            
            query = f"SELECT * FROM {table_name}"
            if limit:
                query += f" LIMIT {limit}"
            
            df = pd.read_sql(query, self.engine)
            
            print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
            print(f"   Columns: {', '.join(df.columns)}\n")
            
            return df
            
        except Exception as e:
            print(f"❌ Error reading table: {e}")
            return None
    
    def write_table(self, df, table_name, if_exists='replace'):
        """
        Write DataFrame to database table
        
        Args:
            df (pd.DataFrame): Data to write
            table_name (str): Table name
            if_exists (str): Action if table exists ('replace', 'append', 'fail')
        """
        try:
            print(f"💾 Writing to table: {table_name}")
            print(f"   Mode: {if_exists}")
            
            df.to_sql(
                table_name,
                self.engine,
                if_exists=if_exists,
                index=False
            )
            
            print(f"✅ Wrote {len(df)} rows\n")
            
        except Exception as e:
            print(f"❌ Error writing table: {e}")
    
    def create_table(self, table_name, schema):
        """
        Create new table
        
        Args:
            table_name (str): Table name
            schema (str): CREATE TABLE SQL statement
        """
        try:
            print(f"🔨 Creating table: {table_name}")
            
            self.execute_query(schema)
            
            print(f"✅ Table created successfully\n")
            
        except Exception as e:
            print(f"❌ Error creating table: {e}")
    
    def table_exists(self, table_name):
        """Check if table exists"""
        query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = :table_name
        )
        """
        result = self.execute_query(query, {'table_name': table_name})
        return result[0][0] if result else False


def setup_sample_database():
    """Set up sample database with test data"""
    
    print("="*70)
    print("🗄️  SETTING UP SAMPLE DATABASE")
    print("="*70 + "\n")
    
    # Database configuration
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'sales_db',
        'user': 'postgres',
        'password': 'postgres'  # Change this to your password
    }
    
    db = DatabaseManager(db_config)
    
    if not db.connect():
        print("⚠️  Please ensure PostgreSQL is running and credentials are correct")
        print("   Default: user='postgres', password='postgres'")
        return None
    
    # Create customers table
    customers_schema = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(10) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        city VARCHAR(50),
        segment VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    db.create_table('customers', customers_schema)
    
    # Create products table
    products_schema = """
    CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR(10) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        price DECIMAL(10, 2),
        stock_quantity INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    db.create_table('products', products_schema)
    
    # Create orders table
    orders_schema = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        customer_id VARCHAR(10) REFERENCES customers(customer_id),
        product_id VARCHAR(10) REFERENCES products(product_id),
        quantity INTEGER,
        order_date DATE,
        region VARCHAR(20),
        status VARCHAR(20)
    )
    """
    
    db.create_table('orders', orders_schema)
    
    # Insert sample data
    print("📝 Inserting sample data...")
    
    # Customers
    customers_data = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'name': ['Mayurkumar Surani', 'Rahul Sharma', 'Priya Patel', 'Amit Kumar', 'Sneha Desai'],
        'email': ['mayur@example.com', 'rahul@example.com', 'priya@example.com', 
                  'amit@example.com', 'sneha@example.com'],
        'city': ['Pune', 'Mumbai', 'Bangalore', 'Delhi', 'Pune'],
        'segment': ['Premium', 'Gold', 'Premium', 'Silver', 'Gold']
    })
    
    db.write_table(customers_data, 'customers', if_exists='replace')
    
    # Products
    products_data = pd.DataFrame({
        'product_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
        'name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
        'category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
        'price': [75000, 500, 1500, 25000, 2000],
        'stock_quantity': [50, 200, 150, 30, 100]
    })
    
    db.write_table(products_data, 'products', if_exists='replace')
    
    # Orders
    orders_data = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003', 'C001', 'C004', 'C005', 'C002', 'C003'],
        'product_id': ['P001', 'P002', 'P003', 'P004', 'P001', 'P005', 'P003', 'P002'],
        'quantity': [2, 10, 5, 1, 1, 4, 3, 15],
        'order_date': pd.date_range('2025-01-01', periods=8),
        'region': ['West', 'East', 'North', 'West', 'South', 'West', 'East', 'North'],
        'status': ['Delivered', 'Delivered', 'Shipped', 'Delivered', 'Processing', 
                   'Delivered', 'Shipped', 'Delivered']
    })
    
    db.write_table(orders_data, 'orders', if_exists='replace')
    
    print("✅ Sample database setup complete!\n")
    
    return db


def demonstrate_queries(db):
    """Demonstrate various SQL queries"""
    
    print("="*70)
    print("📊 RUNNING SAMPLE QUERIES")
    print("="*70 + "\n")
    
    # Query 1: Simple SELECT
    print("1. All Customers:")
    df_customers = db.read_table('customers')
    if df_customers is not None:
        print(df_customers)
    print()
    
    # Query 2: JOIN query
    print("2. Orders with Customer and Product Details:")
    join_query = """
    SELECT 
        o.order_id,
        c.name as customer_name,
        p.name as product_name,
        o.quantity,
        p.price,
        (o.quantity * p.price) as revenue,
        o.order_date,
        o.region,
        o.status
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN products p ON o.product_id = p.product_id
    ORDER BY o.order_date DESC
    """
    
    df_orders = pd.read_sql(join_query, db.engine)
    print(df_orders)
    print()
    
    # Query 3: Aggregation
    print("3. Revenue by Region:")
    agg_query = """
    SELECT 
        o.region,
        COUNT(*) as order_count,
        SUM(o.quantity * p.price) as total_revenue,
        AVG(o.quantity * p.price) as avg_order_value
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY o.region
    ORDER BY total_revenue DESC
    """
    
    df_region = pd.read_sql(agg_query, db.engine)
    print(df_region)
    print()
    
    # Query 4: Customer segment analysis
    print("4. Revenue by Customer Segment:")
    segment_query = """
    SELECT 
        c.segment,
        COUNT(DISTINCT c.customer_id) as customer_count,
        COUNT(o.order_id) as order_count,
        SUM(o.quantity * p.price) as total_revenue
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN products p ON o.product_id = p.product_id
    GROUP BY c.segment
    ORDER BY total_revenue DESC
    """
    
    df_segment = pd.read_sql(segment_query, db.engine)
    print(df_segment)
    print()
    
    # Save results
    print("💾 Saving query results...")
    os.makedirs('output', exist_ok=True)
    df_orders.to_csv('output/orders_detail.csv', index=False)
    df_region.to_csv('output/revenue_by_region.csv', index=False)
    df_segment.to_csv('output/revenue_by_segment.csv', index=False)
    print("✅ Results saved to output/ directory\n")


if __name__ == "__main__":
    print("="*70)
    print("🗄️  DATABASE OPERATIONS DEMONSTRATION")
    print("="*70 + "\n")
    
    # Setup database
    db = setup_sample_database()
    
    if db:
        # Run queries
        demonstrate_queries(db)
        
        # Disconnect
        db.disconnect()
    
    print("="*70)
    print("✅ DATABASE OPERATIONS COMPLETE")
    print("="*70)