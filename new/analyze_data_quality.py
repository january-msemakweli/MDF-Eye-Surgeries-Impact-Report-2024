import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('operated_eye_va_data.csv')
print(f"Total records: {len(df)}")
print(f"MASASI records: {len(df[df['PHYSICAL ADDRSS'] == 'MASASI'])}")
print("\n" + "="*80)

# Analyze each column for data quality issues
columns_to_check = ['SEX', 'AGE', 'PHYSICAL ADDRSS', 'CONFIRMED PROCEDURE', 'EYE', 
                   'PRE_OP_VA', '1_DAY_POST_OP_VA', '2_WEEKS_POST_OP_VA', '1_MONTH_POST_OP_VA']

for col in columns_to_check:
    print(f"\n📊 COLUMN: {col}")
    print("-" * 50)
    
    if col == 'AGE':
        # Special handling for age
        print("Age statistics:")
        print(df[col].describe())
        print(f"Missing values: {df[col].isnull().sum()}")
        print(f"Non-numeric values:")
        non_numeric = df[~df[col].astype(str).str.match(r'^\d+\.?\d*$', na=False)][col].value_counts()
        if len(non_numeric) > 0:
            print(non_numeric)
        else:
            print("None")
    else:
        # For categorical columns
        value_counts = df[col].value_counts(dropna=False)
        print(f"Total unique values: {len(value_counts)}")
        print("Value frequencies:")
        print(value_counts)
        
        # Check for missing/empty values
        missing = df[col].isnull().sum()
        empty_strings = (df[col] == '').sum()
        print(f"Missing (NaN): {missing}")
        print(f"Empty strings: {empty_strings}")
        
        # Check for whitespace issues
        if df[col].dtype == 'object':
            whitespace_issues = df[col].str.contains(r'^\s+|\s+$', na=False).sum()
            print(f"Values with leading/trailing whitespace: {whitespace_issues}")

print("\n" + "="*80)
print("🔍 MASASI-SPECIFIC ANALYSIS")
print("="*80)

masasi_data = df[df['PHYSICAL ADDRSS'] == 'MASASI']
non_masasi_data = df[df['PHYSICAL ADDRSS'] != 'MASASI']

for col in columns_to_check:
    if col in ['PHYSICAL ADDRSS']:  # Skip location column
        continue
        
    print(f"\n📍 {col} - MASASI vs OTHER LOCATIONS")
    print("-" * 60)
    
    if col == 'AGE':
        continue  # Skip age for now
        
    print("MASASI unique values:")
    masasi_values = masasi_data[col].value_counts(dropna=False)
    print(masasi_values)
    
    print("\nOTHER LOCATIONS unique values:")
    other_values = non_masasi_data[col].value_counts(dropna=False)
    print(other_values)
    
    # Find values that are in MASASI but not in other locations
    masasi_unique = set(masasi_data[col].dropna().unique())
    other_unique = set(non_masasi_data[col].dropna().unique())
    
    masasi_only = masasi_unique - other_unique
    if masasi_only:
        print(f"\n⚠️ VALUES ONLY IN MASASI: {masasi_only}")
    
    other_only = other_unique - masasi_unique
    if other_only:
        print(f"ℹ️ Values only in OTHER locations: {other_only}")

print("\n" + "="*80)
print("📝 SUMMARY OF ISSUES TO FIX")
print("="*80)
