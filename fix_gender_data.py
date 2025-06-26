import pandas as pd

# Read the data
print("Reading data...")
df = pd.read_csv('operated_eye_va_data.csv')

# Check current gender distribution
print("\nCurrent gender distribution:")
print(df['SEX'].value_counts())

# Fix gender data - convert M to Male and F to Female
print("\nFixing gender data...")
df['SEX'] = df['SEX'].replace({'M': 'Male', 'F': 'Female'})

# Check updated gender distribution
print("\nUpdated gender distribution:")
print(df['SEX'].value_counts())

# Save the fixed data
print("\nSaving fixed data...")
df.to_csv('operated_eye_va_data.csv', index=False)
print("Done! Gender data has been fixed in 'operated_eye_va_data.csv'") 