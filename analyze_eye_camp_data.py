import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
import os

# Set style for plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

# Create output directory for visualizations
os.makedirs('visualizations', exist_ok=True)

# Read the data - use the fixed dataset
df = pd.read_csv('operated_eye_va_data.csv')

# Ensure gender data is consistent (M/F should be Male/Female)
df['SEX'] = df['SEX'].replace({'M': 'Male', 'F': 'Female'})

print(f"Total number of patients: {len(df)}")

# Clean up age data and convert to numeric
df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')

# Define age categories
age_bins = [0, 14, 49, 59, 69, 79, 200]
age_labels = ['0-14', '15-49', '50-59', '60-69', '70-79', '80+']
df['Age_Category'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels, right=True)

# 1. Demographic Analysis
print("\n--- DEMOGRAPHIC ANALYSIS ---")

# Gender distribution
gender_counts = df['SEX'].value_counts()
print("\nGender Distribution:")
print(gender_counts)

plt.figure(figsize=(10, 6))
ax = sns.countplot(x='SEX', data=df, palette='viridis')
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

# Age categories
age_category_counts = df['Age_Category'].value_counts().sort_index()
print("\nAge Categories Distribution:")
print(age_category_counts)

plt.figure(figsize=(12, 6))
ax = sns.countplot(x='Age_Category', data=df, order=age_labels, palette='viridis')
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

# Location distribution
location_counts = df['PATIENTS PHYSICAL ADDRSS '].value_counts().head(10)
print("\nTop 10 Patient Locations:")
print(location_counts)

plt.figure(figsize=(14, 8))
ax = sns.countplot(y='PATIENTS PHYSICAL ADDRSS ', data=df, 
                  order=df['PATIENTS PHYSICAL ADDRSS '].value_counts().index[:10],
                  palette='viridis')
plt.title('Top 10 Patient Locations', fontsize=16, fontweight='bold')
plt.xlabel('Number of Patients', fontsize=14)
plt.ylabel('Location', fontsize=14)

# Add count labels on bars
for p in ax.patches:
    ax.annotate(f'{int(p.get_width())}', 
                (p.get_width(), p.get_y() + p.get_height()/2), 
                ha='left', va='center', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/location_distribution.png', dpi=300, bbox_inches='tight')

# Diagnosis distribution
diagnosis_counts = df['DIAGNOSIS'].value_counts()
print("\nDiagnosis Distribution:")
print(diagnosis_counts)

# Filter out EVECERATION for the visualization only
diagnosis_df = df[df['DIAGNOSIS'] != 'EVECERATION'].copy()

plt.figure(figsize=(14, 10))
ax = sns.countplot(y='DIAGNOSIS', data=diagnosis_df,
                  order=diagnosis_df['DIAGNOSIS'].value_counts().index,
                  palette='viridis')
plt.title('Diagnosis Distribution', fontsize=16)
plt.xlabel('Number of Patients', fontsize=14)
plt.ylabel('Diagnosis', fontsize=14)

# Add count and percentage labels
total = len(diagnosis_df)
for p in ax.patches:
    width = p.get_width()
    percentage = 100 * width / total
    ax.text(width + 5,
            p.get_y() + p.get_height()/2,
            f'{int(width)} ({percentage:.1f}%)',
            va="center", fontsize=12)

plt.savefig('visualizations/diagnosis_distribution.png', dpi=300, bbox_inches='tight')

# Procedure distribution
procedure_counts = df['CONFIRMED PROCEDURE'].value_counts()
print("\nProcedure Distribution:")
print(procedure_counts)

plt.figure(figsize=(12, 6))
ax = sns.countplot(y='CONFIRMED PROCEDURE', data=df, 
                  order=df['CONFIRMED PROCEDURE'].value_counts().index,
                  palette='viridis')
plt.title('Procedure Distribution', fontsize=16, fontweight='bold')
plt.xlabel('Number of Patients', fontsize=14)
plt.ylabel('Procedure', fontsize=14)

# Add count and percentage labels on bars
total = len(df)
for p in ax.patches:
    width = p.get_width()
    ax.annotate(f'{int(width)} ({width/total:.1%})', 
                (width, p.get_y() + p.get_height()/2), 
                ha='left', va='center', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/procedure_distribution.png', dpi=300, bbox_inches='tight')

# Eye distribution
eye_counts = df['EYE'].value_counts()
print("\nEye Distribution:")
print(eye_counts)

plt.figure(figsize=(10, 6))
ax = sns.countplot(x='EYE', data=df, palette='viridis')
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

# 2. Visual Acuity Analysis
print("\n--- VISUAL ACUITY ANALYSIS ---")

# Identify evisceration cases
evisceration_cases = df[df['CONFIRMED PROCEDURE'] == 'EVISCERATION']
print(f"\nNumber of evisceration cases: {len(evisceration_cases)}")

# VA columns - now only pre-op and 1-month post-op
va_columns = ['PRE_OP_VA', '1_MONTH_POST_OP_VA']

# Get most common VA values for each time point
va_top_values = {}
for col in va_columns:
    va_top_values[col] = df[col].value_counts().head(10)
    print(f"\nTop 10 {col} values:")
    print(va_top_values[col])

# VA distribution by timepoint
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

# Create a stacked bar chart to show progression
# Common VA values across all time points
common_va_values = ['6/6', '6/9', '6/12', '6/18', '6/24', '6/36', '6/60', 'CF6M', 'CF5M', 'CF4M', 'CF3M', 'CF2M', 'CF1M', 'CFN', 'HM', 'PL', 'NPL']

# Filter out evisceration cases for progression analysis
df_non_evisc = df[df['CONFIRMED PROCEDURE'] != 'EVISCERATION']

# Get counts for each value at each time point
va_progression_df = pd.DataFrame()
for col in va_columns:
    # Filter to only include common values
    counts = df_non_evisc[col].value_counts()
    filtered_counts = {}
    for val in common_va_values:
        if val in counts:
            filtered_counts[val] = counts[val]
        else:
            filtered_counts[val] = 0
    
    va_progression_df[col] = pd.Series(filtered_counts)

# Fill NaN with 0
va_progression_df = va_progression_df.fillna(0)

# Normalize to percentage
va_progression_pct = va_progression_df.div(va_progression_df.sum(axis=0), axis=1) * 100

# Plot stacked percentage bar chart
plt.figure(figsize=(14, 8))
va_progression_pct.T.plot(kind='bar', stacked=True, figsize=(14, 8), 
                         colormap='viridis')
plt.title('Visual Acuity Progression Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Time Point', fontsize=14)
plt.ylabel('Percentage of Patients', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='Visual Acuity', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(False)
plt.tight_layout()
plt.savefig('visualizations/va_progression_percentage.png', dpi=300, bbox_inches='tight')

# 3. Improvement Analysis
print("\n--- IMPROVEMENT ANALYSIS ---")

# Define function to convert VA to numeric scale for comparison
# Higher number = better vision
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
    elif va == '6/5':
        return 17
    else:
        return np.nan

# Convert VA to numeric scale
for col in va_columns:
    df[f'{col}_Numeric'] = df[col].apply(va_to_numeric)

# Calculate improvement from pre-op to 1 month post-op
df['Improvement'] = df['1_MONTH_POST_OP_VA_Numeric'] - df['PRE_OP_VA_Numeric']

# Filter out rows with missing improvement data and evisceration cases
improvement_df = df[df['CONFIRMED PROCEDURE'] != 'EVISCERATION'].dropna(subset=['Improvement'])
print(f"\nPatients with complete pre-op and 1-month post-op data (excluding evisceration): {len(improvement_df)}")

# Check if any patients show worsened vision
worse_cases = improvement_df[improvement_df['Improvement'] < 0]
print(f"\nNumber of patients with worsened vision (excluding evisceration): {len(worse_cases)}")
if len(worse_cases) > 0:
    print("\nDetails of patients with worsened vision:")
    print(worse_cases[['DIAGNOSIS', 'CONFIRMED PROCEDURE', 'PRE_OP_VA', '1_MONTH_POST_OP_VA', 'Improvement']])

# Improvement statistics
print("\nImprovement Statistics (Numeric Scale):")
print(improvement_df['Improvement'].describe())

# Categorize improvement
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

# Plot improvement distribution
plt.figure(figsize=(12, 6))
ax = sns.countplot(x='Improvement_Category', data=improvement_df, 
                  order=['Worse', 'No Change', 'Slight Improvement', 
                         'Moderate Improvement', 'Significant Improvement'],
                  palette='viridis')
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

# Add note about special cases if needed
plt.annotate(f'Note: Special cases such as evisceration procedures\nwere appropriately excluded from this analysis.',
            xy=(0.02, 0.02),
            xycoords='axes fraction',
            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3),
            fontsize=10)

plt.tight_layout()
plt.savefig('visualizations/improvement_categories.png', dpi=300, bbox_inches='tight')

# Plot improvement distribution by diagnosis
plt.figure(figsize=(14, 8))
diagnosis_order = df['DIAGNOSIS'].value_counts().index[:5]  # Top 5 diagnoses
sns.boxplot(x='DIAGNOSIS', y='Improvement', data=improvement_df,
           order=diagnosis_order, palette='viridis')
plt.title('Visual Acuity Improvement by Diagnosis', fontsize=16, fontweight='bold')
plt.xlabel('Diagnosis', fontsize=14)
plt.ylabel('Improvement (Numeric Scale)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/improvement_by_diagnosis.png', dpi=300, bbox_inches='tight')

# Plot improvement distribution by age category
plt.figure(figsize=(14, 8))
sns.boxplot(x='Age_Category', y='Improvement', data=improvement_df,
           order=age_labels, palette='viridis')
plt.title('Visual Acuity Improvement by Age Category', fontsize=16, fontweight='bold')
plt.xlabel('Age Category', fontsize=14)
plt.ylabel('Improvement (Numeric Scale)', fontsize=14)
plt.tight_layout()
plt.savefig('visualizations/improvement_by_age.png', dpi=300, bbox_inches='tight')

# Plot improvement distribution by gender
plt.figure(figsize=(10, 6))
sns.boxplot(x='SEX', y='Improvement', data=improvement_df, palette='viridis')
plt.title('Visual Acuity Improvement by Gender', fontsize=16, fontweight='bold')
plt.xlabel('Gender', fontsize=14)
plt.ylabel('Improvement (Numeric Scale)', fontsize=14)
plt.tight_layout()
plt.savefig('visualizations/improvement_by_gender.png', dpi=300, bbox_inches='tight')

# 4. Success Rate Analysis
print("\n--- SUCCESS RATE ANALYSIS ---")

# Define success as achieving 6/18 or better vision at 1 month post-op
# Exclude evisceration cases
df_non_evisc = df[df['CONFIRMED PROCEDURE'] != 'EVISCERATION']
df_non_evisc['Success'] = df_non_evisc['1_MONTH_POST_OP_VA_Numeric'].apply(lambda x: x >= 7 if not pd.isna(x) else np.nan)
success_df = df_non_evisc.dropna(subset=['Success'])

success_rate = success_df['Success'].mean() * 100
print(f"\nOverall Success Rate: {success_rate:.1f}%")

# Success rate by diagnosis
success_by_diagnosis = success_df.groupby('DIAGNOSIS')['Success'].agg(['mean', 'count'])
success_by_diagnosis['mean'] = success_by_diagnosis['mean'] * 100
success_by_diagnosis = success_by_diagnosis.sort_values('count', ascending=False)
print("\nSuccess Rate by Diagnosis:")
print(success_by_diagnosis)

# Plot success rate by diagnosis
plt.figure(figsize=(14, 8))
diagnosis_order = success_by_diagnosis.index[:5]  # Top 5 diagnoses by count
success_by_diagnosis_plot = success_df[success_df['DIAGNOSIS'].isin(diagnosis_order)]

ax = sns.barplot(x='DIAGNOSIS', y='Success', data=success_by_diagnosis_plot,
               order=diagnosis_order, estimator=lambda x: sum(x)/len(x)*100, palette='viridis')
plt.title('Success Rate by Diagnosis (6/18 or Better at 1 Month)', fontsize=16, fontweight='bold')
plt.xlabel('Diagnosis', fontsize=14)
plt.ylabel('Success Rate (%)', fontsize=14)
plt.ylim(0, 100)

# Add count and percentage labels on bars
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height:.1f}%', 
                (p.get_x() + p.get_width()/2., height), 
                ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/success_rate_by_diagnosis.png', dpi=300, bbox_inches='tight')

# Success rate by age category
success_by_age = success_df.groupby('Age_Category')['Success'].agg(['mean', 'count'])
success_by_age['mean'] = success_by_age['mean'] * 100
print("\nSuccess Rate by Age Category:")
print(success_by_age)

# Plot success rate by age category
plt.figure(figsize=(14, 8))
ax = sns.barplot(x='Age_Category', y='Success', data=success_df,
               order=age_labels, estimator=lambda x: sum(x)/len(x)*100, palette='viridis')
plt.title('Success Rate by Age Category (6/18 or Better at 1 Month)', fontsize=16, fontweight='bold')
plt.xlabel('Age Category', fontsize=14)
plt.ylabel('Success Rate (%)', fontsize=14)
plt.ylim(0, 100)

# Add count and percentage labels on bars
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height:.1f}%', 
                (p.get_x() + p.get_width()/2., height), 
                ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/success_rate_by_age.png', dpi=300, bbox_inches='tight')

# Success rate by gender
success_by_gender = success_df.groupby('SEX')['Success'].agg(['mean', 'count'])
success_by_gender['mean'] = success_by_gender['mean'] * 100
print("\nSuccess Rate by Gender:")
print(success_by_gender)

# Plot success rate by gender
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='SEX', y='Success', data=success_df,
               estimator=lambda x: sum(x)/len(x)*100, palette='viridis')
plt.title('Success Rate by Gender (6/18 or Better at 1 Month)', fontsize=16, fontweight='bold')
plt.xlabel('Gender', fontsize=14)
plt.ylabel('Success Rate (%)', fontsize=14)
plt.ylim(0, 100)

# Add count and percentage labels on bars
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height:.1f}%', 
                (p.get_x() + p.get_width()/2., height), 
                ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/success_rate_by_gender.png', dpi=300, bbox_inches='tight')

# 5. Before-After Analysis for Cataract Patients
print("\n--- BEFORE-AFTER ANALYSIS FOR CATARACT PATIENTS ---")

# Filter for cataract patients and exclude evisceration cases
cataract_df = df[(df['DIAGNOSIS'].str.contains('CATARACT', case=False, na=False)) & 
                (df['CONFIRMED PROCEDURE'] != 'EVISCERATION')]
print(f"\nNumber of cataract patients (excluding evisceration): {len(cataract_df)}")

# Create a transition matrix for the most common VA values
top_va_values = list(set(
    list(cataract_df['PRE_OP_VA'].value_counts().head(8).index) + 
    list(cataract_df['1_MONTH_POST_OP_VA'].value_counts().head(8).index)
))

# Filter out rows with missing values
transition_df = cataract_df.dropna(subset=['PRE_OP_VA', '1_MONTH_POST_OP_VA'])
transition_df = transition_df[
    transition_df['PRE_OP_VA'].isin(top_va_values) & 
    transition_df['1_MONTH_POST_OP_VA'].isin(top_va_values)
]

# Create cross-tabulation
transition_matrix = pd.crosstab(
    transition_df['PRE_OP_VA'], 
    transition_df['1_MONTH_POST_OP_VA'],
    normalize='index'
) * 100

print("\nTransition Matrix (% of patients):")
print(transition_matrix)

# Plot heatmap of transitions
plt.figure(figsize=(14, 10))
sns.heatmap(transition_matrix, annot=True, fmt='.1f', cmap='viridis', linewidths=0.5)
plt.title('Visual Acuity Transition: Pre-Op to 1-Month Post-Op for Cataract Patients', 
          fontsize=16, fontweight='bold')
plt.xlabel('1-Month Post-Op Visual Acuity', fontsize=14)
plt.ylabel('Pre-Op Visual Acuity', fontsize=14)
plt.tight_layout()
plt.savefig('visualizations/va_transition_heatmap.png', dpi=300, bbox_inches='tight')

# Plot before-after paired bar chart for cataract patients
# Calculate the percentage of patients in each VA category before and after
pre_op_counts = cataract_df['PRE_OP_VA'].value_counts().head(10)
post_op_counts = cataract_df['1_MONTH_POST_OP_VA'].value_counts().head(10)

pre_op_pct = pre_op_counts / pre_op_counts.sum() * 100
post_op_pct = post_op_counts / post_op_counts.sum() * 100

# Combine into a DataFrame
before_after_df = pd.DataFrame({
    'Pre-Op': pre_op_pct,
    '1-Month Post-Op': post_op_pct
})

# Plot
plt.figure(figsize=(14, 8))
before_after_df.plot(kind='bar', figsize=(14, 8))
plt.title('Visual Acuity Before and After Surgery for Cataract Patients', 
          fontsize=16, fontweight='bold')
plt.xlabel('Visual Acuity', fontsize=14)
plt.ylabel('Percentage of Patients', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Time Point')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('visualizations/before_after_va_cataract.png', dpi=300, bbox_inches='tight')

print("\nAnalysis complete. All visualizations saved to the 'visualizations' directory.") 