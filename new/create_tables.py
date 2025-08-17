import pandas as pd
import numpy as np
import os

# Load the data
df = pd.read_csv('operated_eye_va_data.csv')

# Define vision categories based on WHO standards (same as original)
def categorize_vision(va):
    if pd.isna(va):
        return np.nan
    if va in ['NPL', 'PL', 'HM', 'CF1M', 'CF2M', 'CF3M', 'CF4M', 'CF5M', 'CF6M', 'CFN']:
        return 'Blind/Severe Visual Impairment'
    elif va in ['6/60', '6/36']:
        return 'Moderate Visual Impairment'
    elif va in ['6/24', '6/18']:
        return 'Mild Visual Impairment'
    elif va in ['6/12', '6/9', '6/6', '6/5']:
        return 'Normal/Near Normal'
    else:
        return np.nan

# Apply vision categorization
df['PreOp_Category'] = df['PRE_OP_VA'].apply(categorize_vision)
df['PostOp_Category'] = df['1_MONTH_POST_OP_VA'].apply(categorize_vision)

# Define functional vision (6/18 or better)
def is_functional_vision(va):
    if pd.isna(va):
        return np.nan
    return 1 if va in ['6/18', '6/12', '6/9', '6/6', '6/5'] else 0

df['PreOp_Functional'] = df['PRE_OP_VA'].apply(is_functional_vision)
df['PostOp_Functional'] = df['1_MONTH_POST_OP_VA'].apply(is_functional_vision)

# Create directory for tables if it doesn't exist
if not os.path.exists('tables'):
    os.makedirs('tables')

# 1. Vision Impact Table (same as index.md)
vision_impact = pd.DataFrame({
    'Vision Status': ['Functional Vision (6/18 or better)', 'Non-functional Vision'],
    'Before Surgery (%)': [
        round(df['PreOp_Functional'].mean() * 100, 1),
        round((1 - df['PreOp_Functional'].mean()) * 100, 1)
    ],
    'After Surgery (%)': [
        round(df['PostOp_Functional'].mean() * 100, 1),
        round((1 - df['PostOp_Functional'].mean()) * 100, 1)
    ],
    'Change (percentage points)': [
        round((df['PostOp_Functional'].mean() - df['PreOp_Functional'].mean()) * 100, 1),
        round((df['PreOp_Functional'].mean() - df['PostOp_Functional'].mean()) * 100, 1)
    ]
})
vision_impact.to_csv('tables/vision_impact.csv', index=False)

# Note: WHO vision categories table removed as it conflicts with our success definition

# 3. Location Success Rates (similar to index.md)
location_success = df.groupby('PHYSICAL ADDRSS').agg(
    Total_Patients=('PostOp_Functional', 'count'),
    Success_Count=('PostOp_Functional', 'sum')
).reset_index()

location_success['Success_Rate (%)'] = round(location_success['Success_Count'] / location_success['Total_Patients'] * 100, 1)
location_success.rename(columns={'PHYSICAL ADDRSS': 'Location'}, inplace=True)
location_success = location_success[['Location', 'Total_Patients', 'Success_Count', 'Success_Rate (%)']]
location_success = location_success.sort_values('Success_Rate (%)', ascending=False)
location_success.to_csv('tables/location_success.csv', index=False)

# 4. Procedure Success Rates (similar to index.md diagnosis success)
procedure_success = df.groupby('CONFIRMED PROCEDURE').agg(
    Total_Patients=('PostOp_Functional', 'count'),
    Success_Count=('PostOp_Functional', 'sum')
).reset_index()

procedure_success['Success_Rate (%)'] = round(procedure_success['Success_Count'] / procedure_success['Total_Patients'] * 100, 1)
procedure_success.rename(columns={'CONFIRMED PROCEDURE': 'Procedure Type'}, inplace=True)
procedure_success = procedure_success[['Procedure Type', 'Total_Patients', 'Success_Count', 'Success_Rate (%)']]
procedure_success = procedure_success.sort_values('Total_Patients', ascending=False)
procedure_success.to_csv('tables/procedure_success.csv', index=False)

# 5. Age Success Rates (same as index.md)
# Convert age to numeric, coercing errors to NaN
df['AGE_Numeric'] = pd.to_numeric(df['AGE'], errors='coerce')

# Use the same age categories as in the visualizations
def categorize_age(age):
    if pd.isna(age):
        return np.nan
    elif age < 15:
        return '0-14'
    elif age < 50:
        return '15-49'
    elif age < 60:
        return '50-59'
    elif age < 70:
        return '60-69'
    elif age < 80:
        return '70-79'
    else:
        return '80+'

df['Age_Group'] = df['AGE_Numeric'].apply(categorize_age)

age_success = df.groupby('Age_Group').agg(
    Total_Patients=('PostOp_Functional', 'count'),
    Success_Count=('PostOp_Functional', 'sum')
).reset_index()

# Sort age groups in logical order
age_order = ['0-14', '15-49', '50-59', '60-69', '70-79', '80+']
age_success['Age_Group'] = pd.Categorical(age_success['Age_Group'], categories=age_order, ordered=True)
age_success = age_success.sort_values('Age_Group')

age_success['Success_Rate (%)'] = round(age_success['Success_Count'] / age_success['Total_Patients'] * 100, 1)
age_success.to_csv('tables/age_success.csv', index=False)

# 6. Gender Success Rates (same as index.md)
gender_success = df.groupby('SEX').agg(
    Total_Patients=('PostOp_Functional', 'count'),
    Success_Count=('PostOp_Functional', 'sum')
).reset_index()

gender_success['Success_Rate (%)'] = round(gender_success['Success_Count'] / gender_success['Total_Patients'] * 100, 1)
gender_success.to_csv('tables/gender_success.csv', index=False)

print("All tables have been created in the 'tables' directory, matching index.md structure.")
