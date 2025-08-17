import pandas as pd
import numpy as np

# Read the local dataset
print("Reading operated_eye_va_data.csv...")
df = pd.read_csv('operated_eye_va_data.csv')

print(f"Total number of records: {len(df)}")

# Check current eye distribution
print("\nCurrent eye distribution:")
print(df['EYE'].value_counts(dropna=False))

# Check for any problematic values
print("\nAll unique EYE values:")
print(df['EYE'].unique())

# Clean and standardize eye data
print("\nStandardizing eye data...")

# Remove any extra spaces first
df['EYE'] = df['EYE'].str.strip()

# Replace any problematic values including dots, empty strings, and actual NaN
df['EYE'] = df['EYE'].replace({'.': 'LE', '': 'LE', np.nan: 'LE'})

# Also check for any remaining NaN values and replace with LE
df['EYE'] = df['EYE'].fillna('LE')

print("\nFinal eye distribution after setting missing to LE:")
print(df['EYE'].value_counts(dropna=False))

print(f"\nRemaining missing eye values: {df['EYE'].isna().sum()}")
print(f"All unique values: {df['EYE'].unique()}")

# Save the cleaned dataset
df.to_csv('operated_eye_va_data.csv', index=False)
print("\nEye data fixed with LE. Local dataset saved.")
