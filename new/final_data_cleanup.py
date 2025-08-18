import pandas as pd

# Load the data
df = pd.read_csv('operated_eye_va_data.csv')
print(f"Before cleanup: {len(df)} records")

# Clean gender data
df['SEX'] = df['SEX'].replace({'F': 'Female', 'M': 'Male'})
print("Gender values after cleanup:", df['SEX'].value_counts())

# Clean eye data - remove extra spaces
df['EYE'] = df['EYE'].str.strip()
print("Eye values after cleanup:", df['EYE'].value_counts())

# Save cleaned data
df.to_csv('operated_eye_va_data.csv', index=False)
print("✅ Final data cleanup complete!")

# Show final stats
print(f"\nFinal dataset: {len(df)} records")
print("Final gender distribution:")
print(df['SEX'].value_counts())
print("\nFinal eye distribution:")
print(df['EYE'].value_counts())
print("\nFinal location distribution:")
print(df['PHYSICAL ADDRSS'].value_counts())
