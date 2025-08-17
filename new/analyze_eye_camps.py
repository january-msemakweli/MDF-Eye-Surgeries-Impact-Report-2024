import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

# Create output directory for visualizations
os.makedirs('visualizations', exist_ok=True)
os.makedirs('tables', exist_ok=True)

# Read the data
df = pd.read_csv('operated_eye_va_data.csv')

print(f"Total number of patients: {len(df)}")

# Clean up age data and convert to numeric
df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')

# Define age categories (same as original)
age_bins = [0, 14, 49, 59, 69, 79, 200]
age_labels = ['0-14', '15-49', '50-59', '60-69', '70-79', '80+']
df['Age_Category'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels, right=True)

# 1. Basic Demographics - Same as index.md
print("\n--- DEMOGRAPHIC ANALYSIS ---")

# Gender distribution
gender_counts = df['SEX'].value_counts()
print("\nGender Distribution:")
print(gender_counts)

plt.figure(figsize=(10, 6))
ax = sns.countplot(x='SEX', data=df, palette='viridis', hue='SEX', legend=False)
plt.title('Gender Distribution of Patients', fontsize=16, fontweight='bold')
plt.xlabel('Gender', fontsize=14)
plt.ylabel('Number of Patients', fontsize=14)

# Add count labels on bars
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width()/2., p.get_height()), 
                ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/gender_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Age distribution
print("\nAge Statistics:")
print(df['AGE'].describe())

plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='AGE', bins=20, kde=True)
plt.title('Age Distribution of Patients', fontsize=16, fontweight='bold')
plt.xlabel('Age (Years)', fontsize=14)
plt.ylabel('Number of Patients', fontsize=14)
plt.axvline(df['AGE'].median(), color='red', linestyle='--', label=f'Median Age: {df["AGE"].median():.1f}')
plt.legend()
plt.tight_layout()
plt.savefig('visualizations/age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Age categories
age_category_counts = df['Age_Category'].value_counts().sort_index()
print("\nAge Categories Distribution:")
print(age_category_counts)

plt.figure(figsize=(12, 6))
ax = sns.countplot(x='Age_Category', data=df, order=age_labels, palette='viridis', hue='Age_Category', legend=False)
plt.title('Age Categories of Patients', fontsize=16, fontweight='bold')
plt.xlabel('Age Category', fontsize=14)
plt.ylabel('Number of Patients', fontsize=14)

# Add count and percentage labels on bars
total = len(df)
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{int(height)}\n({height/total:.1%})', 
                (p.get_x() + p.get_width()/2., height), 
                ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/age_categories.png', dpi=300, bbox_inches='tight')
plt.close()

# Location distribution (by physical address)
location_counts = df['PHYSICAL ADDRSS'].value_counts()
print("\nLocation Distribution:")
print(location_counts)

plt.figure(figsize=(14, 8))
ax = sns.countplot(y='PHYSICAL ADDRSS', data=df, 
                  order=df['PHYSICAL ADDRSS'].value_counts().index,
                  palette='viridis', hue='PHYSICAL ADDRSS', legend=False)
plt.title('Geographic Distribution of Patients', fontsize=16, fontweight='bold')
plt.xlabel('Number of Patients', fontsize=14)
plt.ylabel('Location', fontsize=14)

# Add count labels on bars
for p in ax.patches:
    ax.annotate(f'{int(p.get_width())}', 
                (p.get_width(), p.get_y() + p.get_height()/2), 
                ha='left', va='center', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/location_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Procedure distribution
procedure_counts = df['CONFIRMED PROCEDURE'].value_counts()
print("\nProcedure Distribution:")
print(procedure_counts)

plt.figure(figsize=(14, 10))
ax = sns.countplot(y='CONFIRMED PROCEDURE', data=df,
                  order=df['CONFIRMED PROCEDURE'].value_counts().index,
                  palette='viridis', hue='CONFIRMED PROCEDURE', legend=False)
plt.title('Procedure Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Number of Patients', fontsize=14)
plt.ylabel('Procedure', fontsize=14)

# Add count and percentage labels
total = len(df)
for p in ax.patches:
    width = p.get_width()
    percentage = 100 * width / total
    ax.text(width + 5,
            p.get_y() + p.get_height()/2,
            f'{int(width)} ({percentage:.1f}%)',
            va="center", fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/procedure_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Eye distribution
eye_counts = df['EYE'].value_counts()
print("\nEye Distribution:")
print(eye_counts)

plt.figure(figsize=(10, 6))
ax = sns.countplot(x='EYE', data=df, palette='viridis', hue='EYE', legend=False)
plt.title('Eye Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Eye', fontsize=14)
plt.ylabel('Number of Patients', fontsize=14)

# Add count and percentage labels on bars
total = len(df)
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{int(height)}\n({height/total:.1%})', 
                (p.get_x() + p.get_width()/2., height), 
                ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/eye_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Visual Acuity Analysis (basic - matching index.md style)
print("\n--- VISUAL ACUITY ANALYSIS ---")

# Identify evisceration cases
evisceration_cases = df[df['CONFIRMED PROCEDURE'] == 'EVISCERATION']
print(f"\nNumber of evisceration cases: {len(evisceration_cases)}")

# VA distribution by timepoint (same as index.md)
plt.figure(figsize=(14, 8))

# Create subplots for before and after
plt.subplot(1, 2, 1)
preop_counts = df['PRE_OP_VA'].value_counts()
preop_counts = preop_counts.reindex(['6/6', '6/9', '6/12', '6/18', '6/24', '6/36', '6/60', 
                                     'CF6M', 'CF5M', 'CF4M', 'CF3M', 'CF2M', 'CF1M', 'CFN', 'HM', 'PL', 'NPL'])
preop_counts = preop_counts.dropna()
plt.barh(preop_counts.index, preop_counts.values, color='darkred')
plt.title('Pre-Op Visual Acuity', fontsize=16)
plt.xlabel('Number of Patients', fontsize=14)
plt.ylabel('Visual Acuity', fontsize=14)

plt.subplot(1, 2, 2)
postop_counts = df['1_MONTH_POST_OP_VA'].value_counts()
postop_counts = postop_counts.reindex(['6/6', '6/9', '6/12', '6/18', '6/24', '6/36', '6/60', 
                                      'CF6M', 'CF5M', 'CF4M', 'CF3M', 'CF2M', 'CF1M', 'CFN', 'HM', 'PL', 'NPL'])
postop_counts = postop_counts.dropna()
plt.barh(postop_counts.index, postop_counts.values, color='darkgreen')
plt.title('1-Month Post-Op Visual Acuity', fontsize=16)
plt.xlabel('Number of Patients', fontsize=14)

plt.tight_layout()
plt.savefig('visualizations/va_distribution_by_timepoint.png', dpi=300, bbox_inches='tight')
plt.close()

# Improvement Categories (same as index.md)
print("\n--- IMPROVEMENT ANALYSIS ---")

# Define VA to numeric function (same as original)
def va_to_numeric(va):
    if pd.isna(va) or va == '':
        return np.nan
    elif va == 'NPL':
        return 0
    elif va == 'PL':
        return 1
    elif va == 'HM':
        return 2
    elif va == 'CFN':
        return 3
    elif va == 'CF1M':
        return 4
    elif va == 'CF2M':
        return 5
    elif va == 'CF3M':
        return 6
    elif va == 'CF4M':
        return 7
    elif va == 'CF5M':
        return 8
    elif va == 'CF6M':
        return 9
    elif va == '6/60':
        return 10
    elif va == '6/36':
        return 11
    elif va == '6/24':
        return 12
    elif va == '6/18':
        return 13
    elif va == '6/12':
        return 14
    elif va == '6/9':
        return 15
    elif va == '6/6':
        return 16
    else:
        return np.nan

# Convert VA to numeric scale
df['PRE_OP_VA_Numeric'] = df['PRE_OP_VA'].apply(va_to_numeric)
df['1_MONTH_POST_OP_VA_Numeric'] = df['1_MONTH_POST_OP_VA'].apply(va_to_numeric)

# Calculate improvement
df['Improvement'] = df['1_MONTH_POST_OP_VA_Numeric'] - df['PRE_OP_VA_Numeric']

# Filter out evisceration cases for improvement analysis
improvement_df = df[df['CONFIRMED PROCEDURE'] != 'EVISCERATION'].dropna(subset=['Improvement'])
print(f"\nPatients with complete data (excluding evisceration): {len(improvement_df)}")

# Categorize improvement (same as original)
def categorize_improvement(imp):
    if pd.isna(imp):
        return 'Unknown'
    elif imp < 0:
        return 'Worse'
    elif imp == 0:
        return 'No Change'
    elif imp <= 3:
        return 'Slight Improvement'
    elif imp <= 6:
        return 'Moderate Improvement'
    else:
        return 'Significant Improvement'

improvement_df['Improvement_Category'] = improvement_df['Improvement'].apply(categorize_improvement)
improvement_counts = improvement_df['Improvement_Category'].value_counts()
print("\nImprovement Categories:")
print(improvement_counts)

# Plot improvement distribution (same style as index.md)
plt.figure(figsize=(12, 6))
ax = sns.countplot(x='Improvement_Category', data=improvement_df, 
                  order=['Worse', 'No Change', 'Slight Improvement', 
                         'Moderate Improvement', 'Significant Improvement'],
                  palette='viridis', hue='Improvement_Category', legend=False)
plt.title('Visual Acuity Improvement Categories', fontsize=16, fontweight='bold')
plt.xlabel('Improvement Category', fontsize=14)
plt.ylabel('Number of Patients', fontsize=14)

# Add count and percentage labels on bars
total = len(improvement_df)
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{int(height)}\n({height/total:.1%})', 
                (p.get_x() + p.get_width()/2., height), 
                ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/improvement_categories.png', dpi=300, bbox_inches='tight')
plt.close()

print("\nBasic analysis complete. Visualizations saved to the 'visualizations' directory.")
