# text_cleaning.py - Text Data Cleaning and Standardization

import pandas as pd
import re
from colorama import Fore, Style, init

init(autoreset=True)


def create_messy_text_dataset():
    """Create dataset with messy text data"""
    
    data = {
        'customer_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006'],
        'name': [
            'mayurkumar surani',
            'RAHUL SHARMA',
            'Priya  Patel',
            'amit   kumar',
            'Sneha Desai ',
            ' Rohan Mehta'
        ],
        'email': [
            'MAYUR@EXAMPLE.COM',
            'rahul@example.com',
            'priya.patel@EXAMPLE.com',
            'amit@example.com ',
            ' sneha@example.com',
            'rohan@EXAMPLE.COM'
        ],
        'phone': [
            '9876543210',
            '+91-8765432109',
            '91 7654321098',
            '(+91) 6543210987',
            '5432109876',
            '+915432109876'
        ],
        'address': [
            '123, MG Road, Pune, Maharashtra',
            '456 ANDHERI WEST MUMBAI',
            'flat 789, koramangala, bangalore',
            '321, Sector 15, Noida, UP',
            'Plot 654, Banjara Hills, Hyderabad',
            '987, Salt Lake, Kolkata, WB'
        ],
        'comments': [
            'Great product!!! 😊',
            'EXCELLENT SERVICE!!!',
            'good quality... recommended',
            'Fast delivery 🚀 👍',
            'Will buy again!!!',
            'Amazing experience! 5 stars ⭐⭐⭐⭐⭐'
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_csv('messy_text_data.csv', index=False)
    
    print(f"{Fore.GREEN}✅ Created messy text dataset: messy_text_data.csv{Style.RESET_ALL}\n")
    return df


def clean_names(df):
    """Clean and standardize name fields"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"👤 CLEANING NAME FIELDS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_cleaned = df.copy()
    
    print("Original names:")
    print(df_cleaned['name'].tolist())
    print()
    
    # Clean names
    df_cleaned['name_cleaned'] = (
        df_cleaned['name']
        .str.strip()                    # Remove leading/trailing spaces
        .str.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with single space
        .str.title()                    # Title case (First Letter Capitalized)
    )
    
    print("Cleaned names:")
    print(df_cleaned['name_cleaned'].tolist())
    print()
    
    # Extract first and last names
    df_cleaned['first_name'] = df_cleaned['name_cleaned'].str.split().str[0]
    df_cleaned['last_name'] = df_cleaned['name_cleaned'].str.split().str[-1]
    
    print("Extracted components:")
    print(df_cleaned[['name_cleaned', 'first_name', 'last_name']])
    print()
    
    return df_cleaned


def clean_emails(df):
    """Clean and standardize email addresses"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📧 CLEANING EMAIL ADDRESSES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_cleaned = df.copy()
    
    print("Original emails:")
    print(df_cleaned['email'].tolist())
    print()
    
    # Clean emails
    df_cleaned['email_cleaned'] = (
        df_cleaned['email']
        .str.strip()                    # Remove spaces
        .str.lower()                    # Lowercase
    )
    
    print("Cleaned emails:")
    print(df_cleaned['email_cleaned'].tolist())
    print()
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    df_cleaned['email_valid'] = df_cleaned['email_cleaned'].str.match(email_pattern)
    
    print("Email validation:")
    print(df_cleaned[['email_cleaned', 'email_valid']])
    print()
    
    # Extract domain
    df_cleaned['email_domain'] = df_cleaned['email_cleaned'].str.split('@').str[1]
    
    print("Extracted domains:")
    print(df_cleaned['email_domain'].unique())
    print()
    
    return df_cleaned


def clean_phone_numbers(df):
    """Clean and standardize phone numbers"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📱 CLEANING PHONE NUMBERS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_cleaned = df.copy()
    
    print("Original phone numbers:")
    print(df_cleaned['phone'].tolist())
    print()
    
    def standardize_phone(phone):
        """Standardize Indian phone numbers"""
        if pd.isna(phone):
            return None
        
        # Convert to string and remove all non-digits
        phone = str(phone)
        digits = re.sub(r'\D', '', phone)
        
        # Remove country code if present
        if digits.startswith('91') and len(digits) > 10:
            digits = digits[2:]
        
        # Ensure 10 digits
        if len(digits) == 10:
            return digits
        else:
            return None
    
    df_cleaned['phone_cleaned'] = df_cleaned['phone'].apply(standardize_phone)
    
    print("Cleaned phone numbers:")
    print(df_cleaned['phone_cleaned'].tolist())
    print()
    
    # Format for display
    def format_phone(phone):
        """Format phone number for display"""
        if pd.isna(phone) or phone is None:
            return None
        return f"+91 {phone[:5]} {phone[5:]}"
    
    df_cleaned['phone_formatted'] = df_cleaned['phone_cleaned'].apply(format_phone)
    
    print("Formatted phone numbers:")
    print(df_cleaned['phone_formatted'].tolist())
    print()
    
    return df_cleaned


def clean_addresses(df):
    """Clean and standardize addresses"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🏠 CLEANING ADDRESSES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_cleaned = df.copy()
    
    print("Original addresses:")
    for addr in df_cleaned['address']:
        print(f"  {addr}")
    print()
    
    # Clean addresses
    df_cleaned['address_cleaned'] = (
        df_cleaned['address']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.title()
    )
    
    print("Cleaned addresses:")
    for addr in df_cleaned['address_cleaned']:
        print(f"  {addr}")
    print()
    
    # Extract city (assuming it's the second-to-last component)
    df_cleaned['city'] = (
        df_cleaned['address_cleaned']
        .str.split(',')
        .str[-2]
        .str.strip()
    )
    
    print("Extracted cities:")
    print(df_cleaned['city'].tolist())
    print()
    
    return df_cleaned


def clean_text_content(df):
    """Clean text content (comments, reviews, etc.)"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"💬 CLEANING TEXT CONTENT")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_cleaned = df.copy()
    
    print("Original comments:")
    for comment in df_cleaned['comments']:
        print(f"  {comment}")
    print()
    
    def clean_text(text):
        """Clean text content"""
        if pd.isna(text):
            return None
        
        # Remove emojis
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Remove multiple punctuation
        text = re.sub(r'([!?.]){2,}', r'\1', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Strip and capitalize first letter
        text = text.strip()
        if text:
            text = text[0].upper() + text[1:]
        
        return text
    
    df_cleaned['comments_cleaned'] = df_cleaned['comments'].apply(clean_text)
    
    print("Cleaned comments:")
    for comment in df_cleaned['comments_cleaned']:
        print(f"  {comment}")
    print()
    
    # Calculate text length
    df_cleaned['comment_length'] = df_cleaned['comments_cleaned'].str.len()
    
    # Count words
    df_cleaned['comment_words'] = df_cleaned['comments_cleaned'].str.split().str.len()
    
    print("Text statistics:")
    print(df_cleaned[['comments_cleaned', 'comment_length', 'comment_words']])
    print()
    
    return df_cleaned


def remove_special_characters(df):
    """Remove or replace special characters"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔤 REMOVING SPECIAL CHARACTERS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_cleaned = df.copy()
    
    # Example: Clean product names with special characters
    test_products = [
        'Laptop (15")',
        'Mouse - Wireless',
        'Keyboard & Mouse Combo',
        'Monitor 24" LED',
        'Headphones [Noise Cancelling]'
    ]
    
    print("Original product names:")
    for product in test_products:
        print(f"  {product}")
    print()
    
    def clean_product_name(name):
        """Clean product names"""
        # Replace special characters with spaces
        name = re.sub(r'[^\w\s]', ' ', name)
        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name)
        return name.strip()
    
    cleaned_products = [clean_product_name(p) for p in test_products]
    
    print("Cleaned product names:")
    for product in cleaned_products:
        print(f"  {product}")
    print()


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{'='*70}")
    print(f"🧼 TEXT DATA CLEANING DEMONSTRATION")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create messy text dataset
    df = create_messy_text_dataset()
    
    print("Original Dataset:")
    print(df)
    print()
    
    # Clean names
    df = clean_names(df)
    
    # Clean emails
    df = clean_emails(df)
    
    # Clean phone numbers
    df = clean_phone_numbers(df)
    
    # Clean addresses
    df = clean_addresses(df)
    
    # Clean text content
    df = clean_text_content(df)
    
    # Remove special characters
    remove_special_characters(df)
    
    # Save cleaned data
    df.to_csv('output/cleaned_text_data.csv', index=False)
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"✅ TEXT DATA CLEANING COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}")