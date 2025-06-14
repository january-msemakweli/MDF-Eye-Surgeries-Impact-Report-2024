import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create visualizations directory if it doesn't exist
os.makedirs('visualizations', exist_ok=True)

# Read the data
df = pd.read_csv('operated_eye_va_data.csv')

# Filter for cataract patients only
cataract_df = df[df['DIAGNOSIS'].str.contains('CATARACT', case=False, na=False)]
print(f"Number of cataract patients: {len(cataract_df)}")

# Define the ordered VA values from best to worst
ordered_va = ['6/6', '6/9', '6/12', '6/18', '6/24', '6/36', '6/60', 'CF1M', 'CF2M', 'CF3M', 'CF4M', 'CF5M', 'CF6M', 'CFN', 'HM', 'PL', 'NPL']

# Count occurrences of each VA value at pre-op and 1-month post-op
pre_op_counts = cataract_df['PRE_OP_VA'].value_counts()
post_op_counts = cataract_df['1_MONTH_POST_OP_VA'].value_counts()

# Calculate percentages
pre_op_pct = pre_op_counts / pre_op_counts.sum() * 100
post_op_pct = post_op_counts / post_op_counts.sum() * 100

# Create a DataFrame with ordered VA values
va_df = pd.DataFrame({
    'VA': ordered_va,
    'Pre-Op': [pre_op_pct.get(va, 0) for va in ordered_va],
    '1-Month Post-Op': [post_op_pct.get(va, 0) for va in ordered_va]
})

# Reverse the order for plotting (to have best vision at the bottom)
va_df = va_df.iloc[::-1]

# Create the plot
plt.figure(figsize=(16, 10))

# Set width of bars
barWidth = 0.4

# Set positions of the bars on X axis
r1 = np.arange(len(va_df))
r2 = [x + barWidth for x in r1]

# Create bars
plt.barh(r1, va_df['Pre-Op'], height=barWidth, color='#1f77b4', label='Pre-Op')
plt.barh(r2, va_df['1-Month Post-Op'], height=barWidth, color='#ff7f0e', label='1-Month Post-Op')

# Add labels and title
plt.xlabel('Percentage of Patients', fontsize=14)
plt.ylabel('Visual Acuity', fontsize=14)
plt.title('Visual Acuity Before and After Surgery (Cataract Patients)', fontsize=16, fontweight='bold')

# Adjust y-ticks
plt.yticks([r + barWidth/2 for r in range(len(va_df))], va_df['VA'])

# Create legend
plt.legend(loc='upper right', fontsize=12)

# Add grid for better readability
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Add value labels on bars
for i, v in enumerate(va_df['Pre-Op']):
    if v > 0.5:  # Only show label if percentage is significant
        plt.text(v/2, i, f'{v:.1f}%', color='white', fontweight='bold', ha='center', va='center')

for i, v in enumerate(va_df['1-Month Post-Op']):
    if v > 0.5:  # Only show label if percentage is significant
        plt.text(v/2, i + barWidth, f'{v:.1f}%', color='white', fontweight='bold', ha='center', va='center')

# Add a vertical line at 0
plt.axvline(x=0, color='black', linewidth=0.5)

# Ensure proper spacing
plt.tight_layout()

# Save the figure
plt.savefig('visualizations/before_after_va_cataract_ordered.png', dpi=300, bbox_inches='tight')
print("Ordered VA chart saved to visualizations/before_after_va_cataract_ordered.png") 