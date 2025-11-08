# outlier_detection.py - Outlier Detection and Handling

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from colorama import Fore, Style, init

init(autoreset=True)


def create_dataset_with_outliers():
    """Create dataset with outliers"""
    
    np.random.seed(42)
    
    # Normal data
    normal_data = np.random.normal(50000, 10000, 95)
    
    # Add outliers
    outliers = np.array([150000, 200000, 250000, 300000, 5000])
    
    data = {
        'customer_id': [f'C{i:03d}' for i in range(1, 101)],
        'purchase_amount': np.concatenate([normal_data, outliers]),
        'age': np.concatenate([
            np.random.normal(35, 8, 95),
            np.array([80, 85, 90, 15, 12])  # Age outliers
        ]),
        'order_count': np.concatenate([
            np.random.poisson(5, 95),
            np.array([50, 60, 70, 80, 90])  # Order count outliers
        ])
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data_with_outliers.csv', index=False)
    
    print(f"{Fore.GREEN}✅ Created dataset with outliers: data_with_outliers.csv{Style.RESET_ALL}\n")
    return df


def visualize_outliers(df):
    """Visualize outliers using box plots"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 VISUALIZING OUTLIERS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Box plot for purchase_amount
    axes[0].boxplot(df['purchase_amount'])
    axes[0].set_title('Purchase Amount')
    axes[0].set_ylabel('Amount (₹)')
    
    # Box plot for age
    axes[1].boxplot(df['age'])
    axes[1].set_title('Age')
    axes[1].set_ylabel('Years')
    
    # Box plot for order_count
    axes[2].boxplot(df['order_count'])
    axes[2].set_title('Order Count')
    axes[2].set_ylabel('Orders')
    
    plt.tight_layout()
    plt.savefig('output/outliers_boxplot.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved visualization: output/outliers_boxplot.png\n")
    plt.close()


def detect_outliers_iqr(df, column):
    """Detect outliers using IQR (Interquartile Range) method"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔍 DETECTING OUTLIERS - IQR METHOD ({column})")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Calculate Q1, Q3, and IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    # Define outlier boundaries
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    print(f"Statistics:")
    print(f"  Q1 (25th percentile): {Q1:.2f}")
    print(f"  Q3 (75th percentile): {Q3:.2f}")
    print(f"  IQR: {IQR:.2f}")
    print(f"  Lower bound: {lower_bound:.2f}")
    print(f"  Upper bound: {upper_bound:.2f}")
    print()
    
    # Identify outliers
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    print(f"Outliers found: {len(outliers)}")
    if len(outliers) > 0:
        print(f"\nOutlier values:")
        print(outliers[[column]].sort_values(column))
    print()
    
    return outliers, lower_bound, upper_bound


def detect_outliers_zscore(df, column, threshold=3):
    """Detect outliers using Z-score method"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔍 DETECTING OUTLIERS - Z-SCORE METHOD ({column})")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Calculate Z-scores
    z_scores = np.abs(stats.zscore(df[column]))
    
    # Identify outliers (Z-score > threshold)
    outliers = df[z_scores > threshold]
    
    print(f"Threshold: {threshold} standard deviations")
    print(f"Mean: {df[column].mean():.2f}")
    print(f"Std Dev: {df[column].std():.2f}")
    print()
    
    print(f"Outliers found: {len(outliers)}")
    if len(outliers) > 0:
        print(f"\nOutlier values:")
        outlier_data = outliers[[column]].copy()
        outlier_data['z_score'] = z_scores[z_scores > threshold]
        print(outlier_data.sort_values(column))
    print()
    
    return outliers


def handle_outliers_remove(df, column, lower_bound, upper_bound):
    """Handle outliers by removing them"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🗑️  HANDLING OUTLIERS - REMOVAL ({column})")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"Original shape: {df.shape[0]} rows")
    
    # Remove outliers
    df_cleaned = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    print(f"After removal: {df_cleaned.shape[0]} rows")
    print(f"Rows removed: {df.shape[0] - df_cleaned.shape[0]}")
    print()
    
    return df_cleaned


def handle_outliers_cap(df, column, lower_bound, upper_bound):
    """Handle outliers by capping (winsorization)"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📌 HANDLING OUTLIERS - CAPPING ({column})")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_capped = df.copy()
    
    # Count outliers
    lower_outliers = (df_capped[column] < lower_bound).sum()
    upper_outliers = (df_capped[column] > upper_bound).sum()
    
    print(f"Outliers below lower bound: {lower_outliers}")
    print(f"Outliers above upper bound: {upper_outliers}")
    print()
    
    # Cap outliers
    df_capped[f'{column}_capped'] = df_capped[column].clip(lower=lower_bound, upper=upper_bound)
    
    print(f"Original range: {df[column].min():.2f} to {df[column].max():.2f}")
    print(f"Capped range: {df_capped[f'{column}_capped'].min():.2f} to {df_capped[f'{column}_capped'].max():.2f}")
    print()
    
    return df_capped


def handle_outliers_transform(df, column):
    """Handle outliers using log transformation"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"🔄 HANDLING OUTLIERS - LOG TRANSFORMATION ({column})")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    df_transformed = df.copy()
    
    # Apply log transformation (add 1 to handle zeros)
    df_transformed[f'{column}_log'] = np.log1p(df_transformed[column])
    
    print(f"Original statistics:")
    print(f"  Mean: {df[column].mean():.2f}")
    print(f"  Std Dev: {df[column].std():.2f}")
    print(f"  Skewness: {df[column].skew():.2f}")
    print()
    
    print(f"After log transformation:")
    print(f"  Mean: {df_transformed[f'{column}_log'].mean():.2f}")
    print(f"  Std Dev: {df_transformed[f'{column}_log'].std():.2f}")
    print(f"  Skewness: {df_transformed[f'{column}_log'].skew():.2f}")
    print()
    
    return df_transformed


def compare_methods(df, column):
    """Compare different outlier handling methods"""
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"📊 COMPARING OUTLIER HANDLING METHODS ({column})")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Detect outliers using IQR
    outliers, lower_bound, upper_bound = detect_outliers_iqr(df, column)
    
    # Method 1: Remove outliers
    df_removed = handle_outliers_remove(df, column, lower_bound, upper_bound)
    
    # Method 2: Cap outliers
    df_capped = handle_outliers_cap(df, column, lower_bound, upper_bound)
    
    # Method 3: Transform
    df_transformed = handle_outliers_transform(df, column)
    
    # Compare statistics
    comparison = pd.DataFrame({
        'Method': ['Original', 'Removed', 'Capped', 'Log Transformed'],
        'Count': [
            len(df),
            len(df_removed),
            len(df_capped),
            len(df_transformed)
        ],
        'Mean': [
            df[column].mean(),
            df_removed[column].mean(),
            df_capped[f'{column}_capped'].mean(),
            df_transformed[f'{column}_log'].mean()
        ],
        'Std Dev': [
            df[column].std(),
            df_removed[column].std(),
            df_capped[f'{column}_capped'].std(),
            df_transformed[f'{column}_log'].std()
        ],
        'Min': [
            df[column].min(),
            df_removed[column].min(),
            df_capped[f'{column}_capped'].min(),
            df_transformed[f'{column}_log'].min()
        ],
        'Max': [
            df[column].max(),
            df_removed[column].max(),
            df_capped[f'{column}_capped'].max(),
            df_transformed[f'{column}_log'].max()
        ]
    })
    
    print("Comparison of Methods:")
    print(comparison.to_string(index=False))
    print()


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}{'='*70}")
    print(f"📊 OUTLIER DETECTION AND HANDLING DEMONSTRATION")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Create dataset with outliers
    df = create_dataset_with_outliers()
    
    print("Dataset Statistics:")
    print(df.describe())
    print()
    
    # Visualize outliers
    visualize_outliers(df)
    
    # Detect outliers using IQR
    outliers_iqr, lower, upper = detect_outliers_iqr(df, 'purchase_amount')
    
    # Detect outliers using Z-score
    outliers_zscore = detect_outliers_zscore(df, 'purchase_amount')
    
    # Compare methods
    compare_methods(df, 'purchase_amount')
    
    # Save results
    df.to_csv('output/data_with_outliers_marked.csv', index=False)
    
    print(f"{Fore.GREEN}{'='*70}")
    print(f"✅ OUTLIER DETECTION AND HANDLING COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}")