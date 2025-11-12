# setup_database.py - Setup Sample E-commerce Database

import psycopg2
from psycopg2 import sql
import pandas as pd
from datetime import datetime, timedelta
import random
from colorama import Fore, Style, init

init(autoreset=True)


def create_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="ecommerce_db",
            user="postgres",
            password="postgres"  # Change this to your password
        )
        print(f"{Fore.GREEN}✅ Connected to PostgreSQL{Style.RESET_ALL}\n")
        return conn
    except psycopg2.OperationalError:
        # Database doesn't exist, create it
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="root"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE ecommerce_db")
        cursor.close()
        conn.close()
        
        # Connect to new database
        return create_connection()


def create_tables(conn):
    """Create database tables"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔨 CREATING TABLES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute("""
        DROP TABLE IF EXISTS order_items CASCADE;
        DROP TABLE IF EXISTS orders CASCADE;
        DROP TABLE IF EXISTS products CASCADE;
        DROP TABLE IF EXISTS customers CASCADE;
        DROP TABLE IF EXISTS categories CASCADE;
    """)
    
    # Create categories table
    cursor.execute("""
        CREATE TABLE categories (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Created table: categories")
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            customer_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            city VARCHAR(50),
            state VARCHAR(50),
            country VARCHAR(50) DEFAULT 'India',
            registration_date DATE,
            customer_segment VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Created table: customers")
    
    # Create products table
    cursor.execute("""
        CREATE TABLE products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(200) NOT NULL,
            category_id INTEGER REFERENCES categories(category_id),
            price DECIMAL(10, 2) NOT NULL,
            cost DECIMAL(10, 2) NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Created table: products")
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            order_date DATE NOT NULL,
            order_status VARCHAR(20) NOT NULL,
            payment_method VARCHAR(50),
            shipping_city VARCHAR(50),
            shipping_state VARCHAR(50),
            total_amount DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Created table: orders")
    
    # Create order_items table
    cursor.execute("""
        CREATE TABLE order_items (
            order_item_id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(order_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            discount_percent DECIMAL(5, 2) DEFAULT 0,
            line_total DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Created table: order_items")
    
    conn.commit()
    cursor.close()
    print()


def insert_sample_data(conn):
    """Insert sample data into tables"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📝 INSERTING SAMPLE DATA")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    cursor = conn.cursor()
    
    # Insert categories
    categories = [
        ('Electronics', 'Electronic devices and accessories'),
        ('Clothing', 'Apparel and fashion items'),
        ('Books', 'Books and educational materials'),
        ('Home & Kitchen', 'Home appliances and kitchen items'),
        ('Sports', 'Sports equipment and accessories')
    ]
    
    cursor.executemany(
        "INSERT INTO categories (category_name, description) VALUES (%s, %s)",
        categories
    )
    print(f"✅ Inserted {len(categories)} categories")
    
    # Insert customers
    first_names = ['Mayurkumar', 'Rahul', 'Priya', 'Amit', 'Sneha', 'Rohan', 'Neha', 'Vikram', 'Anjali', 'Karan']
    last_names = ['Surani', 'Sharma', 'Patel', 'Kumar', 'Desai', 'Mehta', 'Singh', 'Gupta', 'Reddy', 'Joshi']
    cities = ['Pune', 'Mumbai', 'Bangalore', 'Delhi', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']
    states = ['Maharashtra', 'Maharashtra', 'Karnataka', 'Delhi', 'Telangana', 'Tamil Nadu', 'West Bengal', 'Gujarat']
    segments = ['Premium', 'Gold', 'Silver', 'Bronze']
    
    customers_data = []
    for i in range(100):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        phone = f"98765{random.randint(10000, 99999)}"
        city_idx = random.randint(0, len(cities) - 1)
        city = cities[city_idx]
        state = states[city_idx]
        reg_date = datetime.now().date() - timedelta(days=random.randint(30, 730))
        segment = random.choice(segments)
        
        customers_data.append((first_name, last_name, email, phone, city, state, reg_date, segment))
    
    cursor.executemany(
        """INSERT INTO customers 
           (first_name, last_name, email, phone, city, state, registration_date, customer_segment) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        customers_data
    )
    print(f"✅ Inserted {len(customers_data)} customers")
    
    # Insert products
    products_data = [
        ('Laptop Dell XPS 15', 1, 125000, 95000, 50),
        ('iPhone 15 Pro', 1, 134900, 110000, 30),
        ('Samsung Galaxy S24', 1, 89999, 70000, 40),
        ('Sony Headphones WH-1000XM5', 1, 29990, 22000, 100),
        ('Apple Watch Series 9', 1, 45900, 35000, 60),
        ('Men Formal Shirt', 2, 1499, 800, 200),
        ('Women Ethnic Dress', 2, 2999, 1500, 150),
        ('Jeans Levis 501', 2, 3999, 2200, 180),
        ('Running Shoes Nike', 2, 5999, 3500, 120),
        ('Winter Jacket', 2, 4999, 2800, 90),
        ('Python Programming Book', 3, 599, 350, 300),
        ('Data Science Handbook', 3, 899, 500, 250),
        ('Fiction Novel', 3, 399, 200, 400),
        ('Microwave Oven', 4, 8999, 6500, 40),
        ('Air Fryer', 4, 5999, 4200, 70),
        ('Pressure Cooker', 4, 2499, 1500, 100),
        ('Mixer Grinder', 4, 3999, 2500, 80),
        ('Cricket Bat', 5, 2999, 1800, 60),
        ('Football', 5, 1299, 700, 150),
        ('Yoga Mat', 5, 799, 400, 200)
    ]
    
    cursor.executemany(
        """INSERT INTO products 
           (product_name, category_id, price, cost, stock_quantity) 
           VALUES (%s, %s, %s, %s, %s)""",
        products_data
    )
    print(f"✅ Inserted {len(products_data)} products")
    
    # Insert orders and order items
    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Cash on Delivery', 'Net Banking']
    order_statuses = ['Delivered', 'Shipped', 'Processing', 'Cancelled']
    
    order_count = 0
    order_item_count = 0
    
    for customer_id in range(1, 101):
        # Each customer makes 1-5 orders
        num_orders = random.randint(1, 5)
        
        for _ in range(num_orders):
            order_date = datetime.now().date() - timedelta(days=random.randint(1, 365))
            order_status = random.choice(order_statuses)
            payment_method = random.choice(payment_methods)
            
            # Get customer's city and state
            cursor.execute(
                "SELECT city, state FROM customers WHERE customer_id = %s",
                (customer_id,)
            )
            shipping_city, shipping_state = cursor.fetchone()
            
            # Insert order
            cursor.execute(
                """INSERT INTO orders 
                   (customer_id, order_date, order_status, payment_method, shipping_city, shipping_state) 
                   VALUES (%s, %s, %s, %s, %s, %s) 
                   RETURNING order_id""",
                (customer_id, order_date, order_status, payment_method, shipping_city, shipping_state)
            )
            order_id = cursor.fetchone()[0]
            order_count += 1
            
            # Add 1-4 items to order
            num_items = random.randint(1, 4)
            order_total = 0
            
            for _ in range(num_items):
                product_id = random.randint(1, 20)
                quantity = random.randint(1, 3)
                
                # Get product price
                cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
                unit_price = cursor.fetchone()[0]
                
                discount = random.choice([0, 5, 10, 15, 20])
                line_total = unit_price * quantity * (1 - discount / 100)
                order_total += line_total
                
                cursor.execute(
                    """INSERT INTO order_items 
                       (order_id, product_id, quantity, unit_price, discount_percent, line_total) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (order_id, product_id, quantity, unit_price, discount, line_total)
                )
                order_item_count += 1
            
            # Update order total
            cursor.execute(
                "UPDATE orders SET total_amount = %s WHERE order_id = %s",
                (order_total, order_id)
            )
    
    print(f"✅ Inserted {order_count} orders")
    print(f"✅ Inserted {order_item_count} order items")
    
    conn.commit()
    cursor.close()
    print()


def create_indexes(conn):
    """Create indexes for better query performance"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"⚡ CREATING INDEXES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    cursor = conn.cursor()
    
    indexes = [
        "CREATE INDEX idx_customers_email ON customers(email)",
        "CREATE INDEX idx_customers_city ON customers(city)",
        "CREATE INDEX idx_customers_segment ON customers(customer_segment)",
        "CREATE INDEX idx_orders_customer ON orders(customer_id)",
        "CREATE INDEX idx_orders_date ON orders(order_date)",
        "CREATE INDEX idx_orders_status ON orders(order_status)",
        "CREATE INDEX idx_order_items_order ON order_items(order_id)",
        "CREATE INDEX idx_order_items_product ON order_items(product_id)",
        "CREATE INDEX idx_products_category ON products(category_id)"
    ]
    
    for idx_sql in indexes:
        cursor.execute(idx_sql)
        print(f"✅ {idx_sql.split('CREATE INDEX ')[1].split(' ON')[0]}")
    
    conn.commit()
    cursor.close()
    print()


def display_summary(conn):
    """Display database summary"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 DATABASE SUMMARY")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    cursor = conn.cursor()
    
    tables = ['categories', 'customers', 'products', 'orders', 'order_items']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table.capitalize()}: {count:,} records")
    
    cursor.close()
    print()


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{'='*70}")
    print(f"🗄️  E-COMMERCE DATABASE SETUP")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create connection
    conn = create_connection()
    
    # Create tables
    create_tables(conn)
    
    # Insert sample data
    insert_sample_data(conn)
    
    # Create indexes
    create_indexes(conn)
    
    # Display summary
    display_summary(conn)
    
    conn.close()
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"✅ DATABASE SETUP COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("You can now connect to the database:")
    print("  Database: ecommerce_db")
    print("  User: postgres")
    print("  Password: postgres")
    print("  Host: localhost")
    print("  Port: 5432")