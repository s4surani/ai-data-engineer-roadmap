# normalization_standardization.py - Data Normalization and Standardization

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from colorama import Fore, Style, init

init(autoreset=True)


def create_sample_dataset():
    """Create sample dataset with different scales"""
    
    np.random.seed(42)
    
    data = {
        'customer_id': [f'C{i:03d}' for i in range(1, 101)],
        'age': np.random.normal(35, 10, 100),
        'salary': np.random.normal(1000000, 300000, 100),
        'purchase_amount': np.random.normal(50000, 15000, 100),
        'order_count': np.random.poisson(5, 100),
        'rating': np.random.uniform(1, 5, 100)
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data_for_scaling.csv', index=False)
    
    print(f"{Fore.GREEN}✅ Created sample dataset: data_for_scaling.csv{Style.RESET_ALL}\n")
    return df


def analyze_scales(df):
    """Analyze the scales of different features"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔍 ANALYZING FEATURE SCALES")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    stats = pd.DataFrame({
        'Feature': numeric_cols,
        'Min': [df[col].min() for col in numeric_cols],
        'Max': [df[col].max() for col in numeric_cols],
        'Mean': [df[col].mean() for col in numeric_cols],
        'Std Dev': [df[col].std() for col in numeric_cols],
        'Range': [df[col].max() - df[col].min() for col in numeric_cols]
    })
    
    print("Feature Statistics:")
    print(stats.to_string(index=False))
    print()
    
    print("⚠️  Notice the different scales:")
    print("   - Age: 15-55 (range ~40)")
    print("   - Salary: 400K-1.6M (range ~1.2M)")
    print("   - Purchase Amount: 20K-80K (range ~60K)")
    print("   - Order Count: 0-15 (range ~15)")
    print("   - Rating: 1-5 (range ~4)")
    print()


def standardization_zscore(df):
    """Standardize features using Z-score (StandardScaler)"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 STANDARDIZATION (Z-SCORE)")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("Formula: z = (x - mean) / std_dev")
    print("Result: Mean = 0, Std Dev = 1")
    print()
    
    # Select numeric columns
    numeric_cols = ['age', 'salary', 'purchase_amount', 'order_count', 'rating']
    
    # Apply StandardScaler
    scaler = StandardScaler()
    df_standardized = df.copy()
    df_standardized[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    print("Before Standardization:")
    print(df[numeric_cols].describe())
    print()
    
    print("After Standardization:")
    print(df_standardized[numeric_cols].describe())
    print()
    
    print("✅ All features now have mean ≈ 0 and std dev ≈ 1")
    print()
    
    return df_standardized


def normalization_minmax(df):
    """Normalize features using Min-Max scaling"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 NORMALIZATION (MIN-MAX)")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("Formula: x_scaled = (x - min) / (max - min)")
    print("Result: All values between 0 and 1")
    print()
    
    # Select numeric columns
    numeric_cols = ['age', 'salary', 'purchase_amount', 'order_count', 'rating']
    
    # Apply MinMaxScaler
    scaler = MinMaxScaler()
    df_normalized = df.copy()
    df_normalized[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    print("Before Normalization:")
    print(df[numeric_cols].describe())
    print()
    
    print("After Normalization:")
    print(df_normalized[numeric_cols].describe())
    print()
    
    print("✅ All features now scaled to [0, 1] range")
    print()
    
    return df_normalized


def robust_scaling(df):
    """Scale features using RobustScaler (robust to outliers)"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 ROBUST SCALING")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("Formula: x_scaled = (x - median) / IQR")
    print("Result: Robust to outliers (uses median and IQR)")
    print()
    
    # Select numeric columns
    numeric_cols = ['age', 'salary', 'purchase_amount', 'order_count', 'rating']
    
    # Apply RobustScaler
    scaler = RobustScaler()
    df_robust = df.copy()
    df_robust[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    print("Before Robust Scaling:")
    print(df[numeric_cols].describe())
    print()
    
    print("After Robust Scaling:")
    print(df_robust[numeric_cols].describe())
    print()
    
    print("✅ Features scaled using median and IQR (robust to outliers)")
    print()
    
    return df_robust


def compare_scaling_methods(df):
    """Compare different scaling methods"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 COMPARING SCALING METHODS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Select one feature for comparison
    feature = 'salary'
    
    # Original
    original = df[feature]
    
    # Standardization
    scaler_std = StandardScaler()
    standardized = scaler_std.fit_transform(df[[feature]]).flatten()
    
    # Normalization
    scaler_norm = MinMaxScaler()
    normalized = scaler_norm.fit_transform(df[[feature]]).flatten()
    
    # Robust
    scaler_robust = RobustScaler()
    robust = scaler_robust.fit_transform(df[[feature]]).flatten()
    
    # Create comparison DataFrame
    comparison = pd.DataFrame({
        'Original': original[:5],
        'Standardized': standardized[:5],
        'Normalized': normalized[:5],
        'Robust': robust[:5]
    })
    
    print(f"Comparison for '{feature}' (first 5 values):")
    print(comparison)
    print()
    
    # Statistics comparison
    stats_comparison = pd.DataFrame({
        'Method': ['Original', 'Standardized', 'Normalized', 'Robust'],
        'Min': [
            original.min(),
            standardized.min(),
            normalized.min(),
            robust.min()
        ],
        'Max': [
            original.max(),
            standardized.max(),
            normalized.max(),
            robust.max()
        ],
        'Mean': [
            original.mean(),
            standardized.mean(),
            normalized.mean(),
            robust.mean()
        ],
        'Std Dev': [
            original.std(),
            standardized.std(),
            normalized.std(),
            robust.std()
        ]
    })
    
    print("Statistics Comparison:")
    print(stats_comparison.to_string(index=False))
    print()


def when_to_use_which():
    """Guide on when to use which scaling method"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📚 WHEN TO USE WHICH SCALING METHOD")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    guide = """
    1. STANDARDIZATION (Z-Score)
       ✅ Use when:
          - Features follow normal distribution
          - For algorithms that assume normally distributed data (Linear Regression, Logistic Regression)
          - When you want to preserve the shape of the distribution
       ❌ Avoid when:
          - Data has many outliers (outliers affect mean and std dev)
    
    2. NORMALIZATION (Min-Max)
       ✅ Use when:
          - You need bounded values (0 to 1)
          - For neural networks (bounded inputs work better)
          - For image processing (pixel values 0-255 → 0-1)
          - When you don't want negative values
       ❌ Avoid when:
          - Data has outliers (outliers affect min and max)
          - You need to preserve the distribution shape
    
    3. ROBUST SCALING
       ✅ Use when:
          - Data has many outliers
          - You want scaling robust to extreme values
          - For financial data (often has outliers)
       ❌ Avoid when:
          - You specifically need bounded values (0-1)
    
    4. NO SCALING
       ✅ Use when:
          - Using tree-based algorithms (Decision Trees, Random Forest, XGBoost)
          - Features are already on similar scales
          - For categorical encoding (one-hot encoded features)
    """
    
    print(guide)


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{'='*70}")
    print(f"🔄 NORMALIZATION AND STANDARDIZATION DEMONSTRATION")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create sample dataset
    df = create_sample_dataset()
    
    # Analyze scales
    analyze_scales(df)
    
    # Standardization
    df_standardized = standardization_zscore(df)
    
    # Normalization
    df_normalized = normalization_minmax(df)
    
    # Robust scaling
    df_robust = robust_scaling(df)
    
    # Compare methods
    compare_scaling_methods(df)
    
    # Guide
    when_to_use_which()
    
    # Save results
    df_standardized.to_csv('output/standardized_data.csv', index=False)
    df_normalized.to_csv('output/normalized_data.csv', index=False)
    df_robust.to_csv('output/robust_scaled_data.csv', index=False)
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"✅ NORMALIZATION AND STANDARDIZATION COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}")