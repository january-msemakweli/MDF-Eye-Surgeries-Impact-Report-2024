import pandas as pd
import re

# Load all the CSV tables
vision_impact = pd.read_csv('tables/vision_impact.csv')
location_success = pd.read_csv('tables/location_success.csv') 
procedure_success = pd.read_csv('tables/procedure_success.csv')

# Read the current markdown file
with open('new.md', 'r', encoding='utf-8') as file:
    content = file.read()

print("🔧 Updating all tables in new.md...")

# Function to convert DataFrame to markdown table with proper formatting
def df_to_markdown_table(df):
    # Create header
    headers = '|| ' + ' | '.join(df.columns) + ' |'
    
    # Create separator with proper alignment
    separators = []
    for col in df.columns:
        if col in ['Total_Patients', 'Success_Count'] or any(x in col.lower() for x in ['(%)', 'rate', 'count', 'before', 'after', 'change']):
            separators.append('-' * 17 + ':')  # Right align numbers
        else:
            separators.append(':' + '-' * 15)  # Left align text
    separator = '||' + '|'.join(separators) + '|'
    
    # Create data rows
    rows = []
    for _, row in df.iterrows():
        formatted_values = []
        for col, val in row.items():
            if col in ['Total_Patients', 'Success_Count']:
                formatted_values.append(f"{int(float(val)):>17}")
            elif any(x in col.lower() for x in ['(%)', 'rate']) and isinstance(val, (int, float)):
                formatted_values.append(f"{val:>17.1f}")
            elif 'percentage points' in col.lower() and isinstance(val, (int, float)):
                formatted_values.append(f"{val:>17.1f}")
            else:
                formatted_values.append(f"{str(val):<17}")
        row_str = '|| ' + ' | '.join(formatted_values) + ' |'
        rows.append(row_str)
    
    return headers + '\n' + separator + '\n' + '\n'.join(rows)

# 1. Update Location Success Table
print("Updating location success table...")
location_table = df_to_markdown_table(location_success)
# Find the location table pattern and replace it
location_pattern = r'\|\| Location.*?\|\| MASASI.*?\|.*?\n'
if re.search(location_pattern, content, re.DOTALL):
    content = re.sub(location_pattern, location_table + '\n', content, flags=re.DOTALL)
    print("✅ Location table updated")
else:
    print("❌ Location table pattern not found")

# 2. Update Vision Impact Table  
print("Updating vision impact table...")
vision_table = df_to_markdown_table(vision_impact)
# Find the vision table pattern and replace it
vision_pattern = r'\|\| Vision Status.*?\|\| Non-functional Vision.*?\|.*?\n'
if re.search(vision_pattern, content, re.DOTALL):
    content = re.sub(vision_pattern, vision_table + '\n', content, flags=re.DOTALL)
    print("✅ Vision impact table updated")
else:
    print("❌ Vision impact table pattern not found")

# 3. Update Procedure Success Table
print("Updating procedure success table...")  
procedure_table = df_to_markdown_table(procedure_success)
# Find the procedure table pattern and replace it
procedure_pattern = r'\|\| Procedure Type.*?\|\| AC WASHOUT.*?\|.*?\n'
if re.search(procedure_pattern, content, re.DOTALL):
    content = re.sub(procedure_pattern, procedure_table + '\n', content, flags=re.DOTALL)
    print("✅ Procedure table updated")
else:
    print("❌ Procedure table pattern not found")

# Save the updated content
with open('new.md', 'w', encoding='utf-8') as file:
    file.write(content)

print("\n✅ ALL TABLES UPDATED IN new.md!")
print("\n📋 Current table data:")
print("\n🏥 Location Success:")
for _, row in location_success.iterrows():
    print(f"  {row['Location']}: {int(row['Total_Patients'])} patients, {row['Success_Rate (%)']}% success")

print("\n👁️ Vision Impact:")
for _, row in vision_impact.iterrows():
    print(f"  {row['Vision Status']}: {row['Before Surgery (%)']}% → {row['After Surgery (%)']}% ({row['Change (percentage points)']} pp)")
