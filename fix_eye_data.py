import pandas as pd

# Read the data
print("Reading data...")
df = pd.read_csv('operated_eye_va_data.csv')

# Check current eye distribution
print("\nCurrent eye distribution:")
print(df['EYE'].value_counts())

# Fix eye data - standardize RE and LE values
print("\nFixing eye data...")
df['EYE'] = df['EYE'].str.strip()  # Remove any leading/trailing spaces
df['EYE'] = df['EYE'].replace({' LE': 'LE', ' RE': 'RE'})  # Remove spaces before LE/RE

# Check updated eye distribution
print("\nUpdated eye distribution:")
print(df['EYE'].value_counts())

# Save the fixed data
print("\nSaving fixed data...")
df.to_csv('operated_eye_va_data.csv', index=False)
print("Done! Eye data has been standardized in 'operated_eye_va_data.csv'") 