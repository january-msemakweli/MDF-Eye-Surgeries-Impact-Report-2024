import pandas as pd
import numpy as np

# Read the data
print("Reading Combined_Eye_Surgery_Dataset.csv...")
df = pd.read_csv('Combined_Eye_Surgery_Dataset.csv')

print(f"Total number of records: {len(df)}")

# Convert age to numeric, coercing errors to NaN
df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')

# Check current age data
print("\nCurrent age data status:")
print(f"Missing age values: {df['AGE'].isna().sum()}")
print(f"Age range: {df['AGE'].min():.1f} to {df['AGE'].max():.1f}")
print("\nAge statistics:")
print(df['AGE'].describe())

# Check for unrealistic age values
unrealistic_ages = df[(df['AGE'] < 1) | (df['AGE'] > 110)]
if len(unrealistic_ages) > 0:
    print(f"\nUnrealistic age values found: {len(unrealistic_ages)}")
    print(unrealistic_ages[['SN', 'AGE', 'SEX']].head(10))

# Impute missing age values
missing_age_count = df['AGE'].isna().sum()
print(f"\nAge values to impute: {missing_age_count}")

if missing_age_count > 0:
    # Strategy 1: Impute based on gender-specific median age
    print("Imputing missing ages using gender-specific median...")
    
    # Calculate median age by gender
    age_by_gender = df.groupby('SEX')['AGE'].median()
    print("Median age by gender:")
    print(age_by_gender)
    
    # Impute missing ages based on gender
    for gender in df['SEX'].unique():
        if pd.notna(gender):
            gender_median = age_by_gender.get(gender, df['AGE'].median())
            mask = (df['SEX'] == gender) & (df['AGE'].isna())
            df.loc[mask, 'AGE'] = gender_median
            imputed_count = mask.sum()
            if imputed_count > 0:
                print(f"Imputed {imputed_count} missing ages for {gender} with median: {gender_median:.1f}")
    
    # For any remaining missing values, use overall median
    remaining_missing = df['AGE'].isna().sum()
    if remaining_missing > 0:
        overall_median = df['AGE'].median()
        df['AGE'] = df['AGE'].fillna(overall_median)
        print(f"Imputed {remaining_missing} remaining missing ages with overall median: {overall_median:.1f}")

# Final age data check
print("\nFinal age data after imputation:")
print(f"Missing age values: {df['AGE'].isna().sum()}")
print(f"Age range: {df['AGE'].min():.1f} to {df['AGE'].max():.1f}")
print("\nFinal age statistics:")
print(df['AGE'].describe())

# Round ages to nearest whole number
df['AGE'] = df['AGE'].round().astype(int)

# Save the cleaned dataset
df.to_csv('Combined_Eye_Surgery_Dataset.csv', index=False)
print("\nAge imputation complete. Dataset saved.")
