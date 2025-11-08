# Article 5: Data Transformation & Cleaning Techniques

## Overview
Production-grade data cleaning and transformation pipeline covering missing values, duplicates, outliers, data types, text cleaning, normalization, and feature engineering.

## What's Included

### 1. Missing Values Handling (`missing_values.py`)
- Statistical imputation (mean, median, mode)
- Forward/backward fill
- Interpolation for time series
- Drop strategies

### 2. Duplicate Detection (`duplicates_handling.py`)
- Exact duplicate removal
- Column-specific deduplication
- Fuzzy duplicate detection
- Smart aggregation

### 3. Data Type Conversions (`data_type_conversions.py`)
- Numeric conversions (handle K/M suffixes)
- Date parsing (multiple formats)
- Boolean standardization
- Memory optimization

### 4. Text Cleaning (`text_cleaning.py`)
- Name standardization
- Email normalization
- Phone number formatting
- Address parsing
- Special character removal

### 5. Outlier Detection (`outlier_detection.py`)
- IQR method
- Z-score method
- Visualization
- Handling strategies (remove, cap, transform)

### 6. Normalization & Standardization (`normalization_standardization.py`)
- StandardScaler (Z-score)
- MinMaxScaler (0-1 range)
- RobustScaler (outlier-resistant)
- When to use which

### 7. Feature Engineering (`feature_engineering.py`)
- Date features (year, month, season, weekend)
- Numeric transformations (log, sqrt, binning)
- Categorical encoding (one-hot, label, frequency)
- Aggregations (customer-level stats)
- Text features (length, word count)
- Interactions (combined features)
- Time-based (lag, rolling, days since)

### 8. Production Pipeline (`production_cleaning_pipeline.py`)
- Complete automated pipeline
- Configurable strategies
- Logging and reporting
- Memory optimization
- JSON audit trail

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt