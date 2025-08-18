import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('operated_eye_va_data.csv')
print(f"Before standardization: {len(df)} records")

# =========================================================================
# 1. FIX GENDER DATA
# =========================================================================
print("\n🔧 FIXING GENDER DATA")
print("Before:")
print(df['SEX'].value_counts(dropna=False))

# Fix the 'M  ' (with spaces) issue
df['SEX'] = df['SEX'].str.strip()  # Remove whitespace
df['SEX'] = df['SEX'].replace({'M': 'Male', 'F': 'Female'})

print("After:")
print(df['SEX'].value_counts(dropna=False))

# =========================================================================
# 2. FIX AGE DATA  
# =========================================================================
print("\n🔧 FIXING AGE DATA")
print("Non-numeric age values:")
non_numeric_age = df[~df['AGE'].astype(str).str.match(r'^\d+\.?\d*$', na=False)]['AGE'].value_counts()
print(non_numeric_age)

# Fix '17D' -> '17'
df['AGE'] = df['AGE'].replace({'17D': '17'})
# Convert to numeric
df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')

print(f"Missing age values after conversion: {df['AGE'].isnull().sum()}")

# =========================================================================
# 3. FIX PROCEDURE DATA
# =========================================================================
print("\n🔧 FIXING PROCEDURE DATA")
print("Before:")
procedure_counts = df['CONFIRMED PROCEDURE'].value_counts()
print(procedure_counts)

# Standardize procedures
procedure_mapping = {
    ' SICS': 'SICS',  # Remove leading space
    'SURGERY': 'SICS',  # Generic surgery -> SICS (assuming cataract surgery)
    'LID CYST EXCISION': 'CYST EXCISION',  # Standardize cyst excision
    'FOREIGN BODY': 'FB',  # Standardize foreign body
}

df['CONFIRMED PROCEDURE'] = df['CONFIRMED PROCEDURE'].replace(procedure_mapping)

print("After:")
print(df['CONFIRMED PROCEDURE'].value_counts())

# =========================================================================
# 4. FIX VISUAL ACUITY DATA
# =========================================================================
print("\n🔧 FIXING VISUAL ACUITY DATA")

# Define VA standardization mapping
va_mapping = {
    # Pre-op issues
    'CFOM': 'CF1M',  # Standardize counting fingers
    'C2M': 'CF2M',   # Standardize counting fingers
    'CN': 'CFN',     # Standardize counting fingers
    
    # Post-op issues  
    'CF1N': 'CF1M',  # Standardize counting fingers
    'C6/24': '6/24', # Fix formatting
    'C/36': '6/36',  # Fix formatting
    'CF6M': 'CF6M',  # Keep as is (actually valid)
    '6CF1M': 'CF1M', # Fix formatting error
    '6//9': '6/9',   # Fix double slash
    '6//6': '6/6',   # Fix double slash
    'Q': np.nan,     # Q seems to mean "quit" or missing follow-up
}

# Apply to all VA columns
va_columns = ['PRE_OP_VA', '1_DAY_POST_OP_VA', '2_WEEKS_POST_OP_VA', '1_MONTH_POST_OP_VA']

for col in va_columns:
    print(f"\nFixing {col}:")
    print("MASASI-specific issues before fix:")
    masasi_issues = df[df['PHYSICAL ADDRSS'] == 'MASASI'][col].value_counts()
    problematic_values = [v for v in va_mapping.keys() if v in masasi_issues.index]
    if problematic_values:
        for val in problematic_values:
            count = masasi_issues.get(val, 0)
            print(f"  {val}: {count} -> {va_mapping[val]}")
    else:
        print("  No issues found")
    
    df[col] = df[col].replace(va_mapping)

# =========================================================================
# 5. FIX EYE DATA - Handle missing values in MASASI
# =========================================================================
print("\n🔧 FIXING EYE DATA")
print("Before:")
print(df['EYE'].value_counts(dropna=False))

# Handle missing eye values in MASASI (2 NaN values)
masasi_missing_eye = df[(df['PHYSICAL ADDRSS'] == 'MASASI') & (df['EYE'].isnull())]
print(f"MASASI records missing EYE data: {len(masasi_missing_eye)}")

# For missing EYE values, let's use the overall distribution to impute
# Current distribution: RE=487, LE=475, so roughly 50.6% RE, 49.4% LE
# Let's alternate the missing values
if len(masasi_missing_eye) > 0:
    missing_indices = masasi_missing_eye.index.tolist()
    for i, idx in enumerate(missing_indices):
        if i % 2 == 0:
            df.loc[idx, 'EYE'] = 'RE'
        else:
            df.loc[idx, 'EYE'] = 'LE'
    print(f"Imputed {len(missing_indices)} missing EYE values")

print("After:")
print(df['EYE'].value_counts(dropna=False))

# =========================================================================
# 6. SAVE STANDARDIZED DATA
# =========================================================================
df.to_csv('operated_eye_va_data.csv', index=False)
print(f"\n✅ STANDARDIZATION COMPLETE!")
print(f"Final dataset: {len(df)} records")

# =========================================================================
# 7. FINAL VERIFICATION
# =========================================================================
print("\n📊 FINAL DATA QUALITY CHECK")
print("="*60)

print("\n Gender distribution:")
print(df['SEX'].value_counts(dropna=False))

print(f"\n Age: {df['AGE'].isnull().sum()} missing values")

print("\n Procedure distribution:")
print(df['CONFIRMED PROCEDURE'].value_counts())

print("\n Eye distribution:")
print(df['EYE'].value_counts(dropna=False))

print("\n Location distribution:")
print(df['PHYSICAL ADDRSS'].value_counts())

# Check for any remaining MASASI-specific unusual values
print("\n🔍 REMAINING MASASI-SPECIFIC ISSUES:")
masasi_data = df[df['PHYSICAL ADDRSS'] == 'MASASI']
non_masasi_data = df[df['PHYSICAL ADDRSS'] != 'MASASI']

for col in va_columns:
    masasi_unique = set(masasi_data[col].dropna().unique())
    other_unique = set(non_masasi_data[col].dropna().unique())
    masasi_only = masasi_unique - other_unique
    if masasi_only:
        print(f"{col}: {masasi_only}")

print("\n✅ Data standardization complete! Ready for analysis regeneration.")
