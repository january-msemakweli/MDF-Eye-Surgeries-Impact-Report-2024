import pandas as pd
import numpy as np

# Read the data
print("Reading Combined_Eye_Surgery_Dataset.csv...")
df = pd.read_csv('Combined_Eye_Surgery_Dataset.csv')

print(f"Total number of records: {len(df)}")

# Check current gender distribution
print("\nCurrent gender distribution:")
print(df['SEX'].value_counts(dropna=False))

# Standardize gender data
print("\nStandardizing gender data...")

# Step 1: Strip any whitespace
df['SEX'] = df['SEX'].astype(str).str.strip()

# Step 2: Handle empty strings and 'nan' values
df['SEX'] = df['SEX'].replace(['', 'nan', 'NaN'], np.nan)

# Step 3: Standardize M/F values
df['SEX'] = df['SEX'].replace({'M': 'Male', 'F': 'Female'})

# Check for any remaining problematic values
remaining_issues = df[~df['SEX'].isin(['Male', 'Female']) & df['SEX'].notna()]
if len(remaining_issues) > 0:
    print(f"\nRemaining non-standard gender values found:")
    print(remaining_issues[['SN', 'SEX']].head(10))

# Handle missing gender values by imputing based on the most common gender
missing_gender_count = df['SEX'].isna().sum()
print(f"\nMissing gender values: {missing_gender_count}")

if missing_gender_count > 0:
    # Impute missing gender with the most common gender in the dataset
    most_common_gender = df['SEX'].mode()[0] if len(df['SEX'].mode()) > 0 else 'Female'
    df['SEX'] = df['SEX'].fillna(most_common_gender)
    print(f"Imputed {missing_gender_count} missing gender values with: {most_common_gender}")

# Final gender distribution
print("\nFinal gender distribution after standardization:")
print(df['SEX'].value_counts(dropna=False))

# Verify no missing values remain
print(f"\nRemaining missing gender values: {df['SEX'].isna().sum()}")

# Save the cleaned dataset
df.to_csv('Combined_Eye_Surgery_Dataset.csv', index=False)
print("\nGender standardization complete. Dataset saved.")
