import pandas as pd
import numpy as np
import os

# Load the data
df = pd.read_csv('operated_eye_va_data_fixed.csv')

# Standardize gender values
df['SEX'] = df['SEX'].replace({'M': 'Male', 'F': 'Female'})

# Define vision categories based on WHO standards
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

# 1. Vision Transformation Table - Overall Impact
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

# 2. Detailed Vision Category Transformation
vision_categories = pd.DataFrame({
    'Vision Category': [
        'Normal/Near Normal (6/12 or better)', 
        'Mild Visual Impairment (6/18)', 
        'Moderate Visual Impairment (6/60, 6/36)', 
        'Blind/Severe Visual Impairment (CF, HM, PL, NPL)'
    ]
})

# Calculate percentages for each category before and after surgery
preop_counts = df['PreOp_Category'].value_counts(normalize=True) * 100
postop_counts = df['PostOp_Category'].value_counts(normalize=True) * 100

# Map to our categories
category_mapping = {
    'Normal/Near Normal': 'Normal/Near Normal (6/12 or better)',
    'Mild Visual Impairment': 'Mild Visual Impairment (6/18)',
    'Moderate Visual Impairment': 'Moderate Visual Impairment (6/60, 6/36)',
    'Blind/Severe Visual Impairment': 'Blind/Severe Visual Impairment (CF, HM, PL, NPL)'
}

# Initialize columns with zeros
vision_categories['Before Surgery (%)'] = 0.0
vision_categories['After Surgery (%)'] = 0.0

# Fill in the values
for cat, mapped_cat in category_mapping.items():
    if cat in preop_counts:
        idx = vision_categories[vision_categories['Vision Category'] == mapped_cat].index[0]
        vision_categories.loc[idx, 'Before Surgery (%)'] = round(preop_counts[cat], 1)
    
    if cat in postop_counts:
        idx = vision_categories[vision_categories['Vision Category'] == mapped_cat].index[0]
        vision_categories.loc[idx, 'After Surgery (%)'] = round(postop_counts[cat], 1)

# Calculate change
vision_categories['Change (percentage points)'] = vision_categories['After Surgery (%)'] - vision_categories['Before Surgery (%)']
vision_categories.to_csv('tables/vision_categories.csv', index=False)

# 3. Procedure Success Rates
procedure_success = df.groupby('CONFIRMED PROCEDURE').agg(
    Total_Patients=('PostOp_Functional', 'count'),
    Success_Count=('PostOp_Functional', 'sum')
).reset_index()

procedure_success['Success_Rate (%)'] = round(procedure_success['Success_Count'] / procedure_success['Total_Patients'] * 100, 1)
procedure_success.rename(columns={'CONFIRMED PROCEDURE': 'Procedure Type'}, inplace=True)
procedure_success = procedure_success[['Procedure Type', 'Total_Patients', 'Success_Count', 'Success_Rate (%)']]
procedure_success.to_csv('tables/procedure_success.csv', index=False)

# 4. Diagnosis Success Rates
diagnosis_success = df.groupby('DIAGNOSIS').agg(
    Total_Patients=('PostOp_Functional', 'count'),
    Success_Count=('PostOp_Functional', 'sum')
).reset_index()

diagnosis_success['Success_Rate (%)'] = round(diagnosis_success['Success_Count'] / diagnosis_success['Total_Patients'] * 100, 1)
diagnosis_success.rename(columns={'DIAGNOSIS': 'Diagnosis Type'}, inplace=True)
diagnosis_success = diagnosis_success[['Diagnosis Type', 'Total_Patients', 'Success_Count', 'Success_Rate (%)']]
diagnosis_success.to_csv('tables/diagnosis_success.csv', index=False)

# 5. Demographic Success Rates
# Gender success rates
gender_success = df.groupby('SEX').agg(
    Total_Patients=('PostOp_Functional', 'count'),
    Success_Count=('PostOp_Functional', 'sum')
).reset_index()

gender_success['Success_Rate (%)'] = round(gender_success['Success_Count'] / gender_success['Total_Patients'] * 100, 1)
gender_success.to_csv('tables/gender_success.csv', index=False)

# Age group success rates
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

# 6. Location Success Rates
location_success = df.groupby('PATIENTS PHYSICAL ADDRSS ').agg(
    Total_Patients=('PostOp_Functional', 'count'),
    Success_Count=('PostOp_Functional', 'sum')
).reset_index()

location_success['Success_Rate (%)'] = round(location_success['Success_Count'] / location_success['Total_Patients'] * 100, 1)
location_success.rename(columns={'PATIENTS PHYSICAL ADDRSS ': 'Location'}, inplace=True)
location_success.to_csv('tables/location_success.csv', index=False)

print("All impact tables have been created in the 'tables' directory.") 