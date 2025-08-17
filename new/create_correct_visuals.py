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
df = pd.read_csv('operated_eye_va_data.csv')

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

# ALL TIME POINTS
va_columns = ['PRE_OP_VA', '1_DAY_POST_OP_VA', '2_WEEKS_POST_OP_VA', '1_MONTH_POST_OP_VA']
timepoint_labels = ['Pre-Operation', '1-Day Post-Op', '2-Weeks Post-Op', '1-Month Post-Op']

# Convert VA to numeric scale for all time points
for col in va_columns:
    df[f'{col}_Numeric'] = df[col].apply(va_to_numeric)

# Filter for cataract patients and exclude evisceration cases
cataract_df = df[(df['CONFIRMED PROCEDURE'].str.contains('SICS', case=False, na=False)) & 
                (df['CONFIRMED PROCEDURE'] != 'EVISCERATION')]

print(f"Total cataract patients: {len(cataract_df)}")

# 1. VA DISTRIBUTION AREA CHART (ALL TIME POINTS)
print("Creating VA distribution area chart for ALL time points...")

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
    va_distribution[timepoint_labels[i]] = pd.Series(category_counts)

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

# 2. VA DISTRIBUTION BY TIMEPOINT (ALL TIME POINTS) 
print("Creating VA distribution by timepoint for ALL time points...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

for i, (col, timepoint) in enumerate(zip(va_columns, timepoint_labels)):
    # Count occurrences of each VA value
    va_counts = cataract_df[col].value_counts()
    
    # Create ordered data
    ordered_va = ['6/6', '6/9', '6/12', '6/18', '6/24', '6/36', '6/60', 'CF', 'HM', 'PL', 'NPL']
    ordered_counts = []
    
    for va in ordered_va:
        if va == 'CF':
            # Sum all CF variants
            cf_count = sum([va_counts.get(cf_va, 0) for cf_va in va_counts.index if str(cf_va).startswith('CF')])
            ordered_counts.append(cf_count)
        else:
            ordered_counts.append(va_counts.get(va, 0))
    
    # Create the bar chart
    axes[i].bar(range(len(ordered_va)), ordered_counts, color='steelblue')
    axes[i].set_title(f'{timepoint}', fontsize=14, fontweight='bold')
    axes[i].set_xlabel('Visual Acuity', fontsize=12)
    axes[i].set_ylabel('Number of Patients', fontsize=12)
    axes[i].set_xticks(range(len(ordered_va)))
    axes[i].set_xticklabels(ordered_va, rotation=45)
    axes[i].grid(True, alpha=0.3)

plt.suptitle('Visual Acuity Distribution at Each Time Point', fontsize=18, fontweight='bold')
plt.tight_layout()

# Save the figure
plt.savefig('visualizations/va_distribution_by_timepoint.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. VA JOURNEY FOR CATARACT PATIENTS - OVERALL
print("Creating overall VA journey for cataract patients...")

# Get median VA at each time point
median_va_overall = {}
for col in [f'{c}_Numeric' for c in va_columns]:
    median_va_overall[col] = cataract_df[col].dropna().median()

# Create a dataframe for the journey
journey_df_overall = pd.DataFrame({
    'Time Point': timepoint_labels,
    'Median VA': [median_va_overall[f'{c}_Numeric'] for c in va_columns]
})

# Define VA labels for the y-axis
va_labels = ['NPL', 'PL', 'HM', 'CF', '6/60', '6/36', '6/24', '6/18', '6/12', '6/9', '6/6']

# Create the overall journey chart
plt.figure(figsize=(14, 8))
sns.lineplot(x='Time Point', y='Median VA', data=journey_df_overall, marker='o', markersize=12, linewidth=3, color='#1f77b4')

# Add annotations for each point
for i, row in journey_df_overall.iterrows():
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
plt.title('Visual Acuity Journey for Cataract Patients - Overall', fontsize=18, fontweight='bold')
plt.xlabel('Time Point', fontsize=14)
plt.ylabel('Visual Acuity', fontsize=14)

# Add grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Add a horizontal line at 6/18 (functional vision)
plt.axhline(y=7, color='green', linestyle='--', alpha=0.7, label='Functional Vision (6/18)')

# Add a horizontal line at 6/60 (legal blindness threshold)
plt.axhline(y=4, color='red', linestyle='--', alpha=0.7, label='Legal Blindness Threshold (6/60)')

plt.legend(fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure
plt.savefig('visualizations/va_journey_cataract.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. VA JOURNEY FOR CATARACT PATIENTS BY LOCATION (ALL TIME POINTS)
print("Creating VA journey charts by location for ALL time points...")

locations = df['PHYSICAL ADDRSS'].unique()
locations = sorted([loc for loc in locations if pd.notna(loc)])

for location in locations:
    # Filter for cataract patients in this location
    location_cataract_df = cataract_df[cataract_df['PHYSICAL ADDRSS'] == location].copy()
    
    if len(location_cataract_df) < 5:  # Skip locations with too few cataract patients
        print(f"Skipping {location} - only {len(location_cataract_df)} cataract patients")
        continue
    
    print(f"Creating VA journey for {location} - {len(location_cataract_df)} cataract patients")
    
    # Get median VA at each time point
    median_va = {}
    for col in [f'{c}_Numeric' for c in va_columns]:
        median_va[col] = location_cataract_df[col].dropna().median()

    # Create a dataframe for the journey
    journey_df = pd.DataFrame({
        'Time Point': timepoint_labels,
        'Median VA': [median_va[f'{c}_Numeric'] for c in va_columns]
    })

    # Create the journey chart
    plt.figure(figsize=(14, 8))
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
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the figure
    location_safe = location.replace('/', '_').replace(' ', '_')
    plt.savefig(f'visualizations/va_journey_cataract_{location_safe}.png', dpi=300, bbox_inches='tight')
    plt.close()

print("All visualizations created successfully with ALL TIME POINTS!")
print("Files created:")
print("- va_distribution_area_chart.png (ALL 4 time points)")
print("- va_distribution_by_timepoint.png (ALL 4 time points)")
print("- va_journey_cataract.png (overall, ALL 4 time points)")
print("- va_journey_cataract_[LOCATION].png (for each location, ALL 4 time points)")
