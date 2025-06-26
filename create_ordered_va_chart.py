import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create visualizations directory if it doesn't exist
os.makedirs('visualizations', exist_ok=True)

# Read the data - use the fixed dataset
df = pd.read_csv('operated_eye_va_data.csv')

# Ensure gender data is consistent (M/F should be Male/Female)
df['SEX'] = df['SEX'].replace({'M': 'Male', 'F': 'Female'})

# Filter for cataract patients only and exclude evisceration cases
cataract_df = df[(df['DIAGNOSIS'].str.contains('CATARACT', case=False, na=False)) & 
                (df['CONFIRMED PROCEDURE'] != 'EVISCERATION')]
print(f"Number of cataract patients (excluding evisceration): {len(cataract_df)}")

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

print("\nOrdered VA Counts and Percentages:")
print(ordered_va_counts)

# Calculate the percentage of patients with 6/18 or better vision
better_than_618_pre_op = sum(ordered_va_counts.loc[['6/6', '6/9', '6/12', '6/18'], 'Pre-Op']) / total_pre_op * 100
better_than_618_post_op = sum(ordered_va_counts.loc[['6/6', '6/9', '6/12', '6/18'], '1-Month Post-Op']) / total_post_op * 100

print(f"\nPercentage of patients with 6/18 or better vision:")
print(f"  Pre-Op: {better_than_618_pre_op:.1f}%")
print(f"  1-Month Post-Op: {better_than_618_post_op:.1f}%")
print(f"  Improvement: {better_than_618_post_op - better_than_618_pre_op:.1f} percentage points")

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

# Add annotations for important bars (6/18 or better)
functional_vision_levels = ['6/6', '6/9', '6/12', '6/18']
for i, va in enumerate(ordered_va):
    if va in functional_vision_levels:
        pre_op_value = ordered_va_counts.loc[va, 'Pre-Op %']
        post_op_value = ordered_va_counts.loc[va, '1-Month Post-Op %']
        
        if pre_op_value > 1:  # Only annotate if value is above 1%
            plt.annotate(f'{pre_op_value:.1f}%', 
                        (i - width/2, pre_op_value), 
                        textcoords="offset points",
                        xytext=(0, 5),
                        ha='center',
                        fontsize=10)
            
        if post_op_value > 1:  # Only annotate if value is above 1%
            plt.annotate(f'{post_op_value:.1f}%', 
                        (i + width/2, post_op_value), 
                        textcoords="offset points",
                        xytext=(0, 5),
                        ha='center',
                        fontsize=10)

# Add a legend
plt.legend(fontsize=12)

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

plt.tight_layout()

# Save the figure
plt.savefig('visualizations/before_after_va_cataract_ordered.png', dpi=300, bbox_inches='tight')
print("Ordered VA chart saved to visualizations/before_after_va_cataract_ordered.png") 