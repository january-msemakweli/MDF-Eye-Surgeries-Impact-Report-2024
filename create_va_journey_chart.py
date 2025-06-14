import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create visualizations directory if it doesn't exist
os.makedirs('visualizations', exist_ok=True)

# Set style for plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

# Read the data
df = pd.read_csv('operated_eye_va_data.csv')

# Filter for cataract patients only
cataract_df = df[df['DIAGNOSIS'].str.contains('CATARACT', case=False, na=False)]
print(f"Number of cataract patients: {len(cataract_df)}")

# Define function to convert VA to numeric scale
def va_to_numeric(va):
    if pd.isna(va) or va == '':
        return np.nan
    elif va == 'NPL':
        return 0
    elif va == 'PL':
        return 1
    elif va == 'HM':
        return 2
    elif va.startswith('CF'):
        return 3
    elif va == '6/60':
        return 4
    elif va == '6/36':
        return 5
    elif va == '6/24':
        return 6
    elif va == '6/18':
        return 7
    elif va == '6/12':
        return 8
    elif va == '6/9':
        return 9
    elif va == '6/6':
        return 10
    else:
        return np.nan

# Convert VA to numeric scale
va_columns = ['PRE_OP_VA', '1_DAY_POST_OP_VA', '2_WEEKS_POST_OP_VA', '1_MONTH_POST_OP_VA']
for col in va_columns:
    cataract_df[f'{col}_Numeric'] = cataract_df[col].apply(va_to_numeric)

# Get median VA at each time point
median_va = {}
for col in [f'{c}_Numeric' for c in va_columns]:
    median_va[col] = cataract_df[col].median()

print("Median VA values at each time point:")
for col, value in median_va.items():
    print(f"{col}: {value}")

# Create a dataframe for the journey
journey_df = pd.DataFrame({
    'Time Point': ['Pre-Operation', '1 Day Post-Op', '2 Weeks Post-Op', '1 Month Post-Op'],
    'Median VA': [median_va[f'{c}_Numeric'] for c in va_columns]
})

# Define VA labels for the y-axis
va_labels = ['NPL', 'PL', 'HM', 'CF', '6/60', '6/36', '6/24', '6/18', '6/12', '6/9', '6/6']

# Create the journey chart
plt.figure(figsize=(12, 8))
sns.lineplot(x='Time Point', y='Median VA', data=journey_df, marker='o', markersize=12, linewidth=3, color='#1f77b4')

# Add annotations for each point
for i, row in journey_df.iterrows():
    va_value = row['Median VA']
    va_label = va_labels[int(va_value)]
    plt.annotate(f'{va_label}', 
                 (row['Time Point'], va_value),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center',
                 fontsize=12,
                 fontweight='bold')

# Set y-axis ticks and labels
plt.yticks(range(11), va_labels)

# Add title and labels
plt.title('Visual Acuity Journey for Cataract Patients', fontsize=18, fontweight='bold')
plt.xlabel('Time Point', fontsize=14)
plt.ylabel('Visual Acuity', fontsize=14)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add a horizontal line at 6/12 (functional vision)
plt.axhline(y=8, color='green', linestyle='--', alpha=0.7, label='Functional Vision (6/12)')

# Add a horizontal line at 6/60 (legal blindness threshold)
plt.axhline(y=4, color='red', linestyle='--', alpha=0.7, label='Legal Blindness Threshold (6/60)')

plt.legend(fontsize=12)
plt.tight_layout()

# Save the figure
plt.savefig('visualizations/va_journey_cataract.png', dpi=300, bbox_inches='tight')
print("VA journey chart saved to visualizations/va_journey_cataract.png")

# Create a stacked area chart showing the distribution of VA values at each time point
# Convert VA categories to percentages at each time point
va_categories = ['NPL', 'PL', 'HM', 'CF', '6/60', '6/36', '6/24', '6/18', '6/12', '6/9', '6/6']
va_distribution = pd.DataFrame()

for i, col in enumerate(va_columns):
    # Count occurrences of each VA value
    va_counts = cataract_df[col].value_counts()
    
    # Initialize counts for each category
    category_counts = {cat: 0 for cat in va_categories}
    
    # Update counts based on actual data
    for va, count in va_counts.items():
        if pd.isna(va) or va == '':
            continue
        elif va == 'NPL':
            category_counts['NPL'] += count
        elif va == 'PL':
            category_counts['PL'] += count
        elif va == 'HM':
            category_counts['HM'] += count
        elif va.startswith('CF'):
            category_counts['CF'] += count
        elif va == '6/60':
            category_counts['6/60'] += count
        elif va == '6/36':
            category_counts['6/36'] += count
        elif va == '6/24':
            category_counts['6/24'] += count
        elif va == '6/18':
            category_counts['6/18'] += count
        elif va == '6/12':
            category_counts['6/12'] += count
        elif va == '6/9':
            category_counts['6/9'] += count
        elif va == '6/6':
            category_counts['6/6'] += count
    
    # Add to dataframe
    va_distribution[journey_df['Time Point'][i]] = pd.Series(category_counts)

# Calculate percentages
va_distribution_pct = va_distribution.div(va_distribution.sum(axis=0), axis=1) * 100

# Create the stacked area chart
plt.figure(figsize=(14, 10))

# Define a color palette that shows improvement (red to green)
colors = plt.cm.RdYlGn(np.linspace(0.1, 0.9, len(va_categories)))

# Plot stacked area chart
va_distribution_pct.T.plot(kind='area', stacked=True, figsize=(14, 10), 
                          color=colors)

plt.title('Distribution of Visual Acuity Over Time (Cataract Patients)', fontsize=18, fontweight='bold')
plt.xlabel('Time Point', fontsize=14)
plt.ylabel('Percentage of Patients', fontsize=14)
plt.legend(title='Visual Acuity', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(False)
plt.tight_layout()

# Save the figure
plt.savefig('visualizations/va_distribution_area_chart.png', dpi=300, bbox_inches='tight')
print("VA distribution area chart saved to visualizations/va_distribution_area_chart.png") 