import pandas as pd

# Load and check the current dataset
df = pd.read_csv('operated_eye_va_data.csv')
print(f"Total records: {len(df)}")
print("\nLocation distribution:")
location_counts = df['PHYSICAL ADDRSS'].value_counts()
print(location_counts)

# Check if MASASI data exists
masasi_data = df[df['PHYSICAL ADDRSS'] == 'MASASI']
print(f"\nMASASI records: {len(masasi_data)}")

if len(masasi_data) > 0:
    print("✅ MASASI data is present")
    print("Sample MASASI records:")
    print(masasi_data[['SEX', 'AGE', 'PHYSICAL ADDRSS', 'CONFIRMED PROCEDURE', 'EYE']].head())
else:
    print("❌ MASASI data is missing!")
    
    # If missing, let's append it properly
    print("Fixing MASASI data...")
    
    # Load the correct MASASI data
    masasi_correct = pd.read_csv('MASASI___restructured.csv')
    
    # Add SN column to match format
    max_sn = df['SN'].max()
    masasi_correct['SN'] = range(max_sn + 1, max_sn + 1 + len(masasi_correct))
    
    # Ensure column order matches
    masasi_correct = masasi_correct[df.columns]
    
    # Append MASASI data
    df_fixed = pd.concat([df, masasi_correct], ignore_index=True)
    
    # Save corrected data
    df_fixed.to_csv('operated_eye_va_data.csv', index=False)
    print(f"✅ Fixed! New total: {len(df_fixed)} records")
    print("New location distribution:")
    print(df_fixed['PHYSICAL ADDRSS'].value_counts())
