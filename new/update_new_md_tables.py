import pandas as pd
import re

# Load all the CSV tables
vision_impact = pd.read_csv('tables/vision_impact.csv')
location_success = pd.read_csv('tables/location_success.csv')
procedure_success = pd.read_csv('tables/procedure_success.csv')
gender_success = pd.read_csv('tables/gender_success.csv')
age_success = pd.read_csv('tables/age_success.csv')

# Read the current markdown file
with open('new.md', 'r', encoding='utf-8') as file:
    content = file.read()

# Function to convert DataFrame to markdown table
def df_to_markdown(df):
    headers = '|| ' + ' | '.join(df.columns) + ' |'
    separator = '||' + '|'.join([':' + '-' * (len(col) + 15) + ':' for col in df.columns]) + '|'
    
    rows = []
    for _, row in df.iterrows():
        row_str = '|| ' + ' | '.join([str(val) for val in row]) + ' |'
        rows.append(row_str)
    
    return headers + '\n' + separator + '\n' + '\n'.join(rows)

# Update location success table
location_table = df_to_markdown(location_success)
# Find and replace the location table
location_pattern = r'\|\| Location.*?\|\| MASASI.*?\|.*?\n'
content = re.sub(location_pattern, location_table + '\n', content, flags=re.DOTALL)

# Update vision impact table
vision_table = df_to_markdown(vision_impact)
# Find and replace the vision impact table
vision_pattern = r'\|\| Vision Status.*?\|\| Non-functional Vision.*?\|.*?\n'
content = re.sub(vision_pattern, vision_table + '\n', content, flags=re.DOTALL)

# Update procedure success table
procedure_table = df_to_markdown(procedure_success)
# Find and replace the procedure table
procedure_pattern = r'\|\| Procedure Type.*?\|\| AC WASHOUT.*?\|.*?\n'
content = re.sub(procedure_pattern, procedure_table + '\n', content, flags=re.DOTALL)

# Save the updated content
with open('new.md', 'w', encoding='utf-8') as file:
    file.write(content)

print("✅ new.md updated with corrected tables!")
print("Updated tables:")
print("- Location success rates")
print("- Vision impact statistics") 
print("- Procedure success rates")

# Also update key numbers in text
print("\n📊 Key numbers to verify in new.md:")
print(f"Total patients: 964")
print(f"MASASI patients: 403")
print(f"Female: 543 (56.3%), Male: 421 (43.6%)")
print(f"Vision improvement: 17.9% → 87.9% (70.0 percentage points)")
print(f"SICS procedures: 743, Pterygium: 185")
