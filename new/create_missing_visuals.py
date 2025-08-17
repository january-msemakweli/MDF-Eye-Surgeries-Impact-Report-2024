import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

# Read the data
df = pd.read_csv('../Combined_Eye_Surgery_Dataset.csv')

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
va_columns = ['PRE_OP_VA', '1_MONTH_POST_OP_VA']
for col in va_columns:
    df[f'{col}_Numeric'] = df[col].apply(va_to_numeric)

# 1. VA DISTRIBUTION AREA CHART (like index.md)
print("Creating VA distribution area chart...")

# Filter for cataract patients and exclude evisceration cases
cataract_df = df[(df['CONFIRMED PROCEDURE'].str.contains('SICS', case=False, na=False)) & 
                (df['CONFIRMED PROCEDURE'] != 'EVISCERATION')]

# Create a stacked area chart showing the distribution of VA values at each time point
va_categories = ['NPL', 'PL', 'HM', 'CF', '6/60', '6/36', '6/24', '6/18', '6/12', '6/9', '6/6']
va_distribution = pd.DataFrame()

journey_timepoints = ['Pre-Operation', '1-Month Post-Op']

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
    va_distribution[journey_timepoints[i]] = pd.Series(category_counts)

# Calculate percentages
va_distribution_pct = va_distribution.div(va_distribution.sum(axis=0), axis=1) * 100

# Create the stacked area chart
plt.figure(figsize=(14, 10))

# Define a color palette that shows improvement (red to green)
colors = plt.cm.RdYlGn(np.linspace(0.1, 0.9, len(va_categories)))

# Plot stacked area chart
va_distribution_pct.T.plot(kind='area', stacked=True, figsize=(14, 10), 
                          color=colors)

plt.title('Distribution of Visual Acuity Over Time for Cataract Patients', fontsize=18, fontweight='bold')
plt.xlabel('Time Point', fontsize=14)
plt.ylabel('Percentage of Patients', fontsize=14)
plt.legend(title='Visual Acuity', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(False)
plt.tight_layout()

# Save the figure
plt.savefig('visualizations/va_distribution_area_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. VA JOURNEY FOR CATARACT PATIENTS BY LOCATION
print("Creating VA journey charts by location...")

locations = df['PHYSICAL ADDRSS'].unique()
locations = sorted([loc for loc in locations if pd.notna(loc)])

for location in locations:
    # Filter for cataract patients in this location
    location_cataract_df = cataract_df[cataract_df['PHYSICAL ADDRSS'] == location].copy()
    
    if len(location_cataract_df) < 10:  # Skip locations with too few cataract patients
        continue
    
    # Get median VA at each time point
    median_va = {}
    for col in [f'{c}_Numeric' for c in va_columns]:
        median_va[col] = location_cataract_df[col].dropna().median()

    # Create a dataframe for the journey
    journey_df = pd.DataFrame({
        'Time Point': ['Pre-Operation', '1 Month Post-Op'],
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
        if not pd.isna(va_value) and 0 <= int(va_value) < len(va_labels):
            va_label = va_labels[int(va_value)]
            plt.annotate(f'{va_label}', 
                         (row['Time Point'], va_value),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center',
                         fontsize=12,
                         fontweight='bold')

    # Set y-axis ticks and labels
    plt.yticks(range(len(va_labels)), va_labels)

    # Add title and labels
    plt.title(f'Visual Acuity Journey for Cataract Patients in {location}', fontsize=18, fontweight='bold')
    plt.xlabel('Time Point', fontsize=14)
    plt.ylabel('Visual Acuity', fontsize=14)

    # Add grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)

    # Add a horizontal line at 6/18 (functional vision)
    plt.axhline(y=7, color='green', linestyle='--', alpha=0.7, label='Functional Vision (6/18)')

    # Add a horizontal line at 6/60 (legal blindness threshold)
    plt.axhline(y=4, color='red', linestyle='--', alpha=0.7, label='Legal Blindness Threshold (6/60)')

    plt.legend(fontsize=12)
    plt.tight_layout()

    # Save the figure
    plt.savefig(f'visualizations/va_journey_cataract_{location}.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. BEFORE/AFTER VA CATARACT ORDERED CHARTS
print("Creating before/after VA cataract ordered charts...")

# Define the ordered VA values from best to worst
ordered_va = ['6/6', '6/9', '6/12', '6/18', '6/24', '6/36', '6/60', 'CF6M', 'CF5M', 'CF4M', 'CF3M', 'CF2M', 'CF1M', 'CFN', 'HM', 'PL', 'NPL']

# Count occurrences of each VA value at pre-op and 1-month post-op
pre_op_counts = cataract_df['PRE_OP_VA'].value_counts()
post_op_counts = cataract_df['1_MONTH_POST_OP_VA'].value_counts()

# Create a DataFrame for ordered VA counts
ordered_va_counts = pd.DataFrame(index=ordered_va)
ordered_va_counts['Pre-Op'] = pre_op_counts.reindex(ordered_va).fillna(0)
ordered_va_counts['1-Month Post-Op'] = post_op_counts.reindex(ordered_va).fillna(0)

# Convert to percentages
total_pre_op = ordered_va_counts['Pre-Op'].sum()
total_post_op = ordered_va_counts['1-Month Post-Op'].sum()
ordered_va_counts['Pre-Op %'] = (ordered_va_counts['Pre-Op'] / total_pre_op) * 100
ordered_va_counts['1-Month Post-Op %'] = (ordered_va_counts['1-Month Post-Op'] / total_post_op) * 100

# Calculate the percentage of patients with 6/18 or better vision
better_than_618_pre_op = sum(ordered_va_counts.loc[['6/6', '6/9', '6/12', '6/18'], 'Pre-Op']) / total_pre_op * 100
better_than_618_post_op = sum(ordered_va_counts.loc[['6/6', '6/9', '6/12', '6/18'], '1-Month Post-Op']) / total_post_op * 100

# Create the ordered bar chart
plt.figure(figsize=(14, 8))

# Create position arrays for the bars
x = np.arange(len(ordered_va))
width = 0.35

# Create the bars
plt.bar(x - width/2, ordered_va_counts['Pre-Op %'], width, label='Pre-Op', color='#ff7f0e')
plt.bar(x + width/2, ordered_va_counts['1-Month Post-Op %'], width, label='1-Month Post-Op', color='#1f77b4')

# Add labels and title
plt.xlabel('Visual Acuity', fontsize=14)
plt.ylabel('Percentage of Patients', fontsize=14)
plt.title('Visual Acuity Before and After Cataract Surgery', fontsize=16, fontweight='bold')

# Set the positions of the x-ticks and labels
plt.xticks(x, ordered_va, rotation=45)

# Add a grid for better readability
plt.grid(True, linestyle='--', alpha=0.7, axis='y')

# Add a vertical line after 6/18 to indicate the functional vision threshold
plt.axvline(x=3.5, color='green', linestyle='--', alpha=0.7)
plt.text(3.5, plt.ylim()[1]*0.9, '6/18 or better\n(Functional Vision)', 
         rotation=90, va='top', ha='right', color='green', fontweight='bold')

# Add annotations for the success rates
plt.annotate(f'Pre-Op: {better_than_618_pre_op:.1f}% with 6/18 or better',
            xy=(0.02, 0.96),
            xycoords='axes fraction',
            bbox=dict(boxstyle="round,pad=0.3", fc="orange", alpha=0.3),
            fontsize=12)

plt.annotate(f'Post-Op: {better_than_618_post_op:.1f}% with 6/18 or better',
            xy=(0.02, 0.90),
            xycoords='axes fraction',
            bbox=dict(boxstyle="round,pad=0.3", fc="blue", alpha=0.3),
            fontsize=12)

plt.annotate(f'Improvement: +{better_than_618_post_op - better_than_618_pre_op:.1f} percentage points',
            xy=(0.02, 0.84),
            xycoords='axes fraction',
            bbox=dict(boxstyle="round,pad=0.3", fc="green", alpha=0.3),
            fontsize=12)

# Add a legend
plt.legend(fontsize=12)
plt.tight_layout()

# Save the figure
plt.savefig('visualizations/before_after_va_cataract_ordered.png', dpi=300, bbox_inches='tight')
plt.close()

print("All missing visualizations created successfully!")
print("Files created:")
print("- va_distribution_area_chart.png")
print("- va_journey_cataract_[LOCATION].png (for each location)")
print("- before_after_va_cataract_ordered.png")
