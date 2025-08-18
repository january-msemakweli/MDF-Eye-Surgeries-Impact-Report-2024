import pandas as pd

# Load the current dataset
df = pd.read_csv('operated_eye_va_data.csv')
print(f"Original dataset: {len(df)} records")
print(f"Original MASASI records: {len(df[df['PHYSICAL ADDRSS'] == 'MASASI'])}")

# Remove all MASASI entries
df_without_masasi = df[df['PHYSICAL ADDRSS'] != 'MASASI'].copy()
print(f"Dataset without MASASI: {len(df_without_masasi)} records")

# Load the correct MASASI data
masasi_correct = pd.read_csv('MASASI___restructured.csv')
print(f"Correct MASASI data: {len(masasi_correct)} records")

# Add SN column to MASASI data to match the format
# Start numbering from where the other data ends
max_sn = df_without_masasi['SN'].max() if not df_without_masasi.empty else 0
masasi_correct['SN'] = range(max_sn + 1, max_sn + 1 + len(masasi_correct))

# Ensure column order matches
masasi_correct = masasi_correct[df.columns]

# Combine the datasets
df_corrected = pd.concat([df_without_masasi, masasi_correct], ignore_index=True)
print(f"Final dataset: {len(df_corrected)} records")
print(f"Final MASASI records: {len(df_corrected[df_corrected['PHYSICAL ADDRSS'] == 'MASASI'])}")

# Save the corrected dataset
df_corrected.to_csv('operated_eye_va_data.csv', index=False)
print("✅ Data corrected and saved!")

# Verify the correction
df_verify = pd.read_csv('operated_eye_va_data.csv')
print(f"\nVerification:")
print(f"Total records: {len(df_verify)}")
print(f"MASASI records: {len(df_verify[df_verify['PHYSICAL ADDRSS'] == 'MASASI'])}")
print("\nLocation distribution:")
print(df_verify['PHYSICAL ADDRSS'].value_counts())
