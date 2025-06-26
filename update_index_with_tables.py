import pandas as pd
import os

def read_csv_as_markdown(file_path):
    """Read a CSV file and convert it to markdown table format"""
    df = pd.read_csv(file_path)
    return df.to_markdown(index=False)

def insert_table_into_markdown(md_content, table_markdown, section_identifier, position_identifier=None):
    """
    Insert a markdown table into the markdown content at a specific position
    
    Parameters:
    - md_content: The original markdown content
    - table_markdown: The table to insert in markdown format
    - section_identifier: The section heading to find
    - position_identifier: Optional text to find within the section for more precise positioning
    
    Returns:
    - Updated markdown content with the table inserted
    """
    # Split the content into lines
    lines = md_content.split('\n')
    
    # Find the section
    section_start = -1
    for i, line in enumerate(lines):
        if section_identifier in line and line.startswith('#'):
            section_start = i
            break
    
    if section_start == -1:
        print(f"Section '{section_identifier}' not found")
        return md_content
    
    # If position identifier is provided, find it within the section
    insert_pos = section_start + 1
    if position_identifier:
        for i in range(section_start, len(lines)):
            if position_identifier in lines[i]:
                # Insert after the line containing the position identifier
                insert_pos = i + 1
                break
    else:
        # Find a good position within the section (after text, before images)
        for i in range(section_start + 1, len(lines)):
            # Stop at the next heading or image
            if lines[i].startswith('#') or '![' in lines[i]:
                insert_pos = i
                break
            # If we're at the end of the file, insert at the end
            if i == len(lines) - 1:
                insert_pos = i + 1
    
    # Insert the table
    lines.insert(insert_pos, "\n" + table_markdown + "\n")
    
    return '\n'.join(lines)

# Read the current index.md content
with open('index.md', 'r') as file:
    md_content = file.read()

# 1. Vision Impact Table
vision_impact_table = read_csv_as_markdown('tables/vision_impact.csv')
md_content = insert_table_into_markdown(
    md_content, 
    vision_impact_table, 
    "Vision Transformation",
    "The surgical interventions achieved remarkable improvements in patients' vision:"
)

# 2. Vision Categories Table
vision_categories_table = read_csv_as_markdown('tables/vision_categories.csv')
md_content = insert_table_into_markdown(
    md_content, 
    vision_categories_table, 
    "Vision Transformation",
    "Dramatic shift from predominantly poor vision to good vision among those who received surgery"
)

# 3. Procedure Success Table
procedure_success_table = read_csv_as_markdown('tables/procedure_success.csv')
md_content = insert_table_into_markdown(
    md_content, 
    procedure_success_table, 
    "Clinical Impact",
    "Procedures matched to community needs, emphasizing cost-effective interventions"
)

# 4. Diagnosis Success Table
diagnosis_success_table = read_csv_as_markdown('tables/diagnosis_success.csv')
md_content = insert_table_into_markdown(
    md_content, 
    diagnosis_success_table, 
    "Clinical Impact",
    "Focus on high-impact conditions that cause the most vision impairment"
)

# 5. Gender Success Table
gender_success_table = read_csv_as_markdown('tables/gender_success.csv')
md_content = insert_table_into_markdown(
    md_content, 
    gender_success_table, 
    "Success Rate Analysis",
    "Equal success rates for males and females, demonstrating gender equity in outcomes"
)

# 6. Age Success Table
age_success_table = read_csv_as_markdown('tables/age_success.csv')
md_content = insert_table_into_markdown(
    md_content, 
    age_success_table, 
    "Success Rate Analysis",
    "Consistent success across all age groups, with highest rates in working-age adults (15-49)"
)

# 7. Location Success Table
location_success_table = read_csv_as_markdown('tables/location_success.csv')
md_content = insert_table_into_markdown(
    md_content, 
    location_success_table, 
    "Community Reach",
    "Geographic distribution shows successful outreach to multiple communities"
)

# Write the updated content back to index.md
with open('index.md', 'w') as file:
    file.write(md_content)

print("Tables have been added to index.md at appropriate locations.") 