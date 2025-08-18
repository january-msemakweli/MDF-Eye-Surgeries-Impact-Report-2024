import pandas as pd

# Load the data
df = pd.read_csv('operated_eye_va_data.csv')

print("=== CURRENT STANDARDIZED DATA STATISTICS ===")
print(f"Total patients: {len(df)}")

# Gender breakdown
female_count = len(df[df['SEX'] == 'Female'])
male_count = len(df[df['SEX'] == 'Male'])
female_pct = female_count / len(df) * 100
male_pct = male_count / len(df) * 100
print(f"Gender: Female {female_count} ({female_pct:.1f}%), Male {male_count} ({male_pct:.1f}%)")

# Age
avg_age = df['AGE'].mean()
print(f"Average age: {avg_age:.1f} years")

# Age categories for 60+ percentage
age_60_plus = len(df[df['AGE'] >= 60])
age_60_plus_pct = age_60_plus / len(df[df['AGE'].notna()]) * 100
print(f"Patients 60+: {age_60_plus} ({age_60_plus_pct:.1f}%)")

# Location breakdown
print("\nLocation distribution:")
location_counts = df['PHYSICAL ADDRSS'].value_counts()
for location, count in location_counts.items():
    print(f"  {location}: {count}")

# Procedure breakdown
print("\nProcedure distribution:")
procedure_counts = df['CONFIRMED PROCEDURE'].value_counts()
sics_count = procedure_counts.get('SICS', 0)
pterygium_count = procedure_counts.get('PTERYGIUM', 0)
sics_pct = sics_count / len(df) * 100
pterygium_pct = pterygium_count / len(df) * 100
print(f"  SICS: {sics_count} ({sics_pct:.1f}%)")
print(f"  PTERYGIUM: {pterygium_count} ({pterygium_pct:.1f}%)")

# Eye distribution
print("\nEye distribution:")
eye_counts = df['EYE'].value_counts()
for eye, count in eye_counts.items():
    print(f"  {eye}: {count}")

print("\n=== VISION STATISTICS ===")
# Load vision impact table
vision_impact = pd.read_csv('tables/vision_impact.csv')
print("Vision transformation:")
for _, row in vision_impact.iterrows():
    print(f"  {row['Vision Status']}: {row['Before Surgery (%)']}% → {row['After Surgery (%)']}% ({row['Change (percentage points)']} pp)")

print("\n=== SUCCESS RATES BY LOCATION ===")
# Load location success table
location_success = pd.read_csv('tables/location_success.csv')
for _, row in location_success.iterrows():
    print(f"  {row['Location']}: {row['Total_Patients']} patients, {row['Success_Rate (%)']}% success rate")
