# feature_engineering.py - Feature Engineering Techniques

import pandas as pd
import numpy as np
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


def create_sample_dataset():
    """Create sample dataset for feature engineering"""
    
    np.random.seed(42)
    
    data = {
        'customer_id': [f'C{i:03d}' for i in range(1, 51)],
        'name': ['Mayurkumar Surani', 'Rahul Sharma', 'Priya Patel'] * 16 + ['Amit Kumar', 'Sneha Desai'],
        'age': np.random.randint(20, 60, 50),
        'salary': np.random.randint(500000, 2000000, 50),
        'purchase_date': pd.date_range('2024-01-01', periods=50, freq='W'),
        'purchase_amount': np.random.randint(10000, 100000, 50),
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], 50),
        'city': np.random.choice(['Pune', 'Mumbai', 'Bangalore', 'Delhi'], 50),
        'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'UPI', 'Cash'], 50)
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data_for_feature_engineering.csv', index=False)
    
    print(f"{Fore.GREEN}✅ Created sample dataset: data_for_feature_engineering.csv{Style.RESET_ALL}\n")
    return df


def create_date_features(df):
    """Create features from date columns"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📅 CREATING DATE-BASED FEATURES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_features = df.copy()
    
    # Ensure date column is datetime
    df_features['purchase_date'] = pd.to_datetime(df_features['purchase_date'])
    
    # Extract date components
    df_features['purchase_year'] = df_features['purchase_date'].dt.year
    df_features['purchase_month'] = df_features['purchase_date'].dt.month
    df_features['purchase_day'] = df_features['purchase_date'].dt.day
    df_features['purchase_weekday'] = df_features['purchase_date'].dt.dayofweek
    df_features['purchase_quarter'] = df_features['purchase_date'].dt.quarter
    df_features['purchase_week_of_year'] = df_features['purchase_date'].dt.isocalendar().week
    
    # Create categorical features
    df_features['is_weekend'] = df_features['purchase_weekday'].isin([5, 6]).astype(int)
    df_features['is_month_start'] = df_features['purchase_date'].dt.is_month_start.astype(int)
    df_features['is_month_end'] = df_features['purchase_date'].dt.is_month_end.astype(int)
    
    # Season (for India)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Summer'
        elif month in [6, 7, 8, 9]:
            return 'Monsoon'
        else:
            return 'Autumn'
    
    df_features['season'] = df_features['purchase_month'].apply(get_season)
    
    print("Created date features:")
    date_features = ['purchase_year', 'purchase_month', 'purchase_day', 'purchase_weekday',
                     'purchase_quarter', 'is_weekend', 'season']
    print(df_features[['purchase_date'] + date_features].head())
    print()
    
    return df_features


def create_numeric_features(df):
    """Create features from numeric columns"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔢 CREATING NUMERIC FEATURES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_features = df.copy()
    
    # Binning (age groups)
    df_features['age_group'] = pd.cut(
        df_features['age'],
        bins=[0, 25, 35, 45, 100],
        labels=['Young', 'Adult', 'Middle-aged', 'Senior']
    )
    
    # Binning (salary brackets)
    df_features['salary_bracket'] = pd.cut(
        df_features['salary'],
        bins=[0, 800000, 1200000, 1600000, 3000000],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Mathematical transformations
    df_features['purchase_amount_log'] = np.log1p(df_features['purchase_amount'])
    df_features['purchase_amount_sqrt'] = np.sqrt(df_features['purchase_amount'])
    df_features['purchase_amount_squared'] = df_features['purchase_amount'] ** 2
    
    # Ratios
    df_features['purchase_to_salary_ratio'] = df_features['purchase_amount'] / df_features['salary']
    
    # Polynomial features
    df_features['age_salary_interaction'] = df_features['age'] * df_features['salary']
    
    print("Created numeric features:")
    numeric_features = ['age_group', 'salary_bracket', 'purchase_amount_log', 
                       'purchase_to_salary_ratio']
    print(df_features[['age', 'salary', 'purchase_amount'] + numeric_features].head())
    print()
    
    return df_features


def create_categorical_features(df):
    """Create features from categorical columns"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📝 CREATING CATEGORICAL FEATURES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_features = df.copy()
    
    # One-hot encoding
    df_encoded = pd.get_dummies(
        df_features,
        columns=['product_category', 'payment_method'],
        prefix=['category', 'payment'],
        drop_first=False
    )
    
    print("One-hot encoded features:")
    encoded_cols = [col for col in df_encoded.columns if col.startswith(('category_', 'payment_'))]
    print(df_encoded[['customer_id'] + encoded_cols[:5]].head())
    print()
    
    # Label encoding (for ordinal data)
    city_mapping = {'Pune': 1, 'Mumbai': 2, 'Bangalore': 3, 'Delhi': 4}
    df_features['city_encoded'] = df_features['city'].map(city_mapping)
    
    # Frequency encoding
    city_freq = df_features['city'].value_counts(normalize=True)
    df_features['city_frequency'] = df_features['city'].map(city_freq)
    
    print("Encoded categorical features:")
    print(df_features[['city', 'city_encoded', 'city_frequency']].head())
    print()
    
    return df_features, df_encoded


def create_aggregation_features(df):
    """Create aggregation-based features"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 CREATING AGGREGATION FEATURES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_features = df.copy()
    
    # Customer-level aggregations
    customer_stats = df_features.groupby('customer_id').agg({
        'purchase_amount': ['count', 'sum', 'mean', 'max', 'min', 'std'],
        'age': 'first',
        'salary': 'first'
    }).reset_index()
    
    # Flatten column names
    customer_stats.columns = ['customer_id', 'purchase_count', 'total_spent', 
                              'avg_purchase', 'max_purchase', 'min_purchase', 
                              'purchase_std', 'age', 'salary']
    
    # Create derived features
    customer_stats['purchase_range'] = customer_stats['max_purchase'] - customer_stats['min_purchase']
    customer_stats['purchase_cv'] = customer_stats['purchase_std'] / customer_stats['avg_purchase']  # Coefficient of variation
    
    # Merge back to original dataframe
    df_features = df_features.merge(customer_stats, on='customer_id', how='left', suffixes=('', '_agg'))
    
    print("Aggregation features:")
    agg_features = ['purchase_count', 'total_spent', 'avg_purchase', 'purchase_range']
    print(df_features[['customer_id'] + agg_features].head())
    print()
    
    return df_features


def create_text_features(df):
    """Create features from text columns"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📝 CREATING TEXT FEATURES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_features = df.copy()
    
    # Name length
    df_features['name_length'] = df_features['name'].str.len()
    
    # Word count
    df_features['name_word_count'] = df_features['name'].str.split().str.len()
    
    # Extract first name
    df_features['first_name'] = df_features['name'].str.split().str[0]
    
    # Check for specific patterns
    df_features['has_kumar'] = df_features['name'].str.contains('Kumar', case=False).astype(int)
    
    print("Text features:")
    text_features = ['name', 'name_length', 'name_word_count', 'first_name', 'has_kumar']
    print(df_features[text_features].head())
    print()
    
    return df_features


def create_interaction_features(df):
    """Create interaction features between multiple columns"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔗 CREATING INTERACTION FEATURES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_features = df.copy()
    
    # Combine categorical features
    df_features['city_category'] = df_features['city'] + '_' + df_features['product_category']
    df_features['city_payment'] = df_features['city'] + '_' + df_features['payment_method']
    
    # Numeric interactions
    df_features['age_purchase_interaction'] = df_features['age'] * df_features['purchase_amount']
    df_features['salary_purchase_ratio'] = df_features['salary'] / (df_features['purchase_amount'] + 1)
    
    print("Interaction features:")
    interaction_features = ['city_category', 'age_purchase_interaction', 'salary_purchase_ratio']
    print(df_features[['city', 'product_category'] + interaction_features].head())
    print()
    
    return df_features


def create_time_based_features(df):
    """Create time-based rolling and lag features"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"⏰ CREATING TIME-BASED FEATURES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_features = df.copy()
    
    # Sort by customer and date
    df_features = df_features.sort_values(['customer_id', 'purchase_date'])
    
    # Lag features (previous purchase amount)
    df_features['prev_purchase'] = df_features.groupby('customer_id')['purchase_amount'].shift(1)
    df_features['prev_2_purchase'] = df_features.groupby('customer_id')['purchase_amount'].shift(2)
    
    # Rolling features (last 3 purchases average)
    df_features['rolling_avg_3'] = (
        df_features.groupby('customer_id')['purchase_amount']
        .rolling(window=3, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )
    
    # Days since last purchase
    df_features['days_since_last_purchase'] = (
        df_features.groupby('customer_id')['purchase_date']
        .diff()
        .dt.days
    )
    
    print("Time-based features:")
    time_features = ['customer_id', 'purchase_date', 'purchase_amount', 
                    'prev_purchase', 'rolling_avg_3', 'days_since_last_purchase']
    print(df_features[time_features].head(10))
    print()
    
    return df_features


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{'='*70}")
    print(f"🎨 FEATURE ENGINEERING DEMONSTRATION")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create sample dataset
    df = create_sample_dataset()
    
    print("Original Dataset:")
    print(df.head())
    print(f"\nOriginal features: {df.shape[1]}")
    print()
    
    # Create date features
    df = create_date_features(df)
    
    # Create numeric features
    df = create_numeric_features(df)
    
    # Create categorical features
    df, df_encoded = create_categorical_features(df)
    
    # Create aggregation features
    df = create_aggregation_features(df)
    
    # Create text features
    df = create_text_features(df)
    
    # Create interaction features
    df = create_interaction_features(df)
    
    # Create time-based features
    df = create_time_based_features(df)
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 FEATURE ENGINEERING SUMMARY")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"Original features: 9")
    print(f"Final features: {df.shape[1]}")
    print(f"New features created: {df.shape[1] - 9}")
    print()
    
    print("Feature categories:")
    print("  ✅ Date features: 10+")
    print("  ✅ Numeric transformations: 7+")
    print("  ✅ Categorical encodings: 8+")
    print("  ✅ Aggregations: 7+")
    print("  ✅ Text features: 4+")
    print("  ✅ Interactions: 4+")
    print("  ✅ Time-based: 4+")
    print()
    
    # Save results
    df.to_csv('output/engineered_features.csv', index=False)
    df_encoded.to_csv('output/encoded_features.csv', index=False)
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"✅ FEATURE ENGINEERING COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}")