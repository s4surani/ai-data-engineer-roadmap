# data_utils/validators.py

import pandas as pd

def schema_validate(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def type_checks(df, col_types):
    for col, typ in col_types.items():
        if col in df.columns:
            wrong_types = ~df[col].apply(lambda x: isinstance(x, typ) or pd.isna(x))
            if wrong_types.any():
                raise TypeError(f"Invalid type in column {col}")

def null_value_handling(df):
    nulls = df.isnull().sum()
    print("Null values in each column:\n", nulls)
    return nulls

def duplicate_detection(df):
    dups = df.duplicated().sum()
    print(f"Duplicate rows: {dups}")
    return dups
