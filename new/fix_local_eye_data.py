import pandas as pd
import numpy as np

# Read the local dataset
print("Reading operated_eye_va_data.csv...")
df = pd.read_csv('operated_eye_va_data.csv')

print(f"Total number of records: {len(df)}")

# Check current eye distribution
print("\nCurrent eye distribution:")
print(df['EYE'].value_counts())

# Clean and standardize eye data
print("\nStandardizing eye data...")

# Remove any extra spaces
df['EYE'] = df['EYE'].str.strip()

# Replace problematic values and missing data
df['EYE'] = df['EYE'].replace({'.': np.nan, '': np.nan})

# Count missing values
missing_eye = df['EYE'].isna().sum()
print(f"\nMissing eye values: {missing_eye}")

if missing_eye > 0:
    # Get the mode (most common value)
    eye_mode = df['EYE'].mode()[0]
    print(f"Eye mode (most common): {eye_mode}")
    
    # Fill missing values with mode
    df.loc[df['EYE'].isna(), 'EYE'] = eye_mode
    print(f"Filled {missing_eye} missing eye values with '{eye_mode}'")

print("\nFinal eye distribution after standardization:")
print(df['EYE'].value_counts())

print(f"\nRemaining missing eye values: {df['EYE'].isna().sum()}")

# Save the cleaned dataset
df.to_csv('operated_eye_va_data.csv', index=False)
print("\nEye data standardization complete. Local dataset saved.")
