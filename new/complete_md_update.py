import pandas as pd

# Load the standardized data
df = pd.read_csv('operated_eye_va_data.csv')

# Calculate all the statistics we need
total_patients = len(df)
female_count = len(df[df['SEX'] == 'Female'])
male_count = len(df[df['SEX'] == 'Male'])
female_pct = female_count / total_patients * 100
male_pct = male_count / total_patients * 100
avg_age = df['AGE'].mean()
age_60_plus = len(df[df['AGE'] >= 60])
age_60_plus_pct = age_60_plus / len(df[df['AGE'].notna()]) * 100

# Location counts
masasi_count = len(df[df['PHYSICAL ADDRSS'] == 'MASASI'])
siha_count = len(df[df['PHYSICAL ADDRSS'] == 'SIHA'])
kivule_count = len(df[df['PHYSICAL ADDRSS'] == 'KIVULE'])
mwanga_count = len(df[df['PHYSICAL ADDRSS'] == 'MWANGA'])

# Procedure counts
sics_count = len(df[df['CONFIRMED PROCEDURE'] == 'SICS'])
pterygium_count = len(df[df['CONFIRMED PROCEDURE'] == 'PTERYGIUM'])
sics_pct = sics_count / total_patients * 100
pterygium_pct = pterygium_count / total_patients * 100

# Eye counts
re_count = len(df[df['EYE'] == 'RE'])
le_count = len(df[df['EYE'] == 'LE'])

# Load table data
vision_impact = pd.read_csv('tables/vision_impact.csv')
location_success = pd.read_csv('tables/location_success.csv')

# Vision statistics
functional_before = vision_impact[vision_impact['Vision Status'] == 'Functional Vision (6/18 or better)']['Before Surgery (%)'].iloc[0]
functional_after = vision_impact[vision_impact['Vision Status'] == 'Functional Vision (6/18 or better)']['After Surgery (%)'].iloc[0]
functional_change = vision_impact[vision_impact['Vision Status'] == 'Functional Vision (6/18 or better)']['Change (percentage points)'].iloc[0]

print("📝 CREATING UPDATED new.md with ALL CORRECT NUMBERS...")

# Create the updated markdown content
content = f"""# Mo Dewji Foundation Eye Camp Surgeries Impact Report: 2025

This report presents the surgical impact of the Mo Dewji Foundation free eye camps conducted in Tanzania during 2025, focusing specifically on surgical interventions that transformed lives through restored vision. The analysis covers {total_patients} surgical patients who underwent procedures across four eye camp locations.

> **Note**: Throughout this report, "Success Rate" refers to the percentage of patients achieving functional vision (visual acuity of 6/18 or better) after surgery, based on World Health Organization standards for vision that enables independent daily activities.

## Key Impact Highlights

- **Surgical Impact**: Eye camp surgeries performed on {total_patients} patients across four locations
- **Geographic Reach**: Surgeries conducted at eye camps in MASASI ({masasi_count} surgeries), SIHA ({siha_count}), KIVULE ({kivule_count}), and MWANGA ({mwanga_count})
- **Primary Interventions**: {sics_count} cataract surgeries (SICS) and {pterygium_count} pterygium excisions performed
- **Gender Equity**: {female_pct:.1f}% female ({female_count}) and {male_pct:.1f}% male ({male_count}) surgical patients, ensuring excellent access for women
- **Age Coverage**: Average age of surgical patients was {avg_age:.1f} years, with services reaching all age groups from children to elderly
- **Vision Restoration**: {functional_after:.1f}% of patients with complete follow-up achieved functional vision after surgery

## Community Reach

The Mo Dewji Foundation eye camp surgeries were performed across four locations in Tanzania, with surgical interventions provided to:

- **Gender Equity**: {female_pct:.1f}% female ({female_count}) and {male_pct:.1f}% male ({male_count}) surgical patients, showing strong access for women
- **Age Range**: Average age of surgical patients was {avg_age:.1f} years, with services reaching all age groups from children to elderly
- **Geographic Access**: Surgeries performed at 4 different eye camp locations, demonstrating surgical outreach to underserved regions

![Gender Distribution](visualizations/gender_distribution.png)
*Excellent gender equity in access to surgical eye care services*

![Age Distribution](visualizations/age_distribution.png)
*Surgical services reached across all age groups, with focus on elderly who have highest prevalence of vision impairment*

![Age Categories](visualizations/age_categories.png)
*Targeted surgical interventions across age groups, with {age_60_plus_pct:.1f}% of surgical patients aged 60 or older*

![Location Distribution](visualizations/location_distribution.png)
*Geographic distribution shows successful outreach to multiple communities*

|| Location       |   Total_Patients |   Success_Count |   Success_Rate (%) |
||:---------------|-----------------:|----------------:|-------------------:|"""

# Add location success table
for _, row in location_success.iterrows():
    content += f"\n|| {row['Location']:<13} |              {int(row['Total_Patients']):>3} |             {int(row['Success_Count']):>3} |               {row['Success_Rate (%)']:>4.1f} |"

content += f"""


![Eye Distribution](visualizations/eye_distribution.png)
*Equal treatment of left and right eyes, demonstrating comprehensive surgical care*

## Clinical Impact

The surgical interventions addressed the most pressing eye health needs in the communities:

- **Addressing Critical Needs**: {sics_pct:.1f}% of surgical cases were cataract ({sics_count}), the leading cause of blindness
- **Comprehensive Care**: {pterygium_pct:.1f}% pterygium cases ({pterygium_count}) and other conditions treated surgically
- **Appropriate Interventions**: Small Incision Cataract Surgery (SICS) - a cost-effective, high-quality approach

![Procedure Distribution](visualizations/procedure_distribution.png)
*Focus on high-impact procedures that address the most common causes of vision impairment*
"""

# Add procedure success table (read from CSV)
procedure_success = pd.read_csv('tables/procedure_success.csv')
content += "\n|| Procedure Type   |   Total_Patients |   Success_Count |   Success_Rate (%) |\n"
content += "||:-----------------|-----------------:|----------------:|-------------------:|\n"
for _, row in procedure_success.iterrows():
    content += f"|| {row['Procedure Type']:<15} |              {int(row['Total_Patients']):>3} |             {int(row['Success_Count']):>3} |               {row['Success_Rate (%)']:>4.1f} |\n"

content += f"""

## Vision Transformation

The surgical interventions achieved remarkable improvements in patients' vision:

|| Vision Status                      |   Before Surgery (%) |   After Surgery (%) |   Change (percentage points) |
||:-----------------------------------|---------------------:|--------------------:|-----------------------------:|"""

# Add vision impact table
for _, row in vision_impact.iterrows():
    content += f"\n|| {row['Vision Status']:<34} |                 {row['Before Surgery (%)']:>4.1f} |                {row['After Surgery (%)']:>4.1f} |                         {row['Change (percentage points)']:>4.1f} |"

content += f"""


- **Functional Vision Gained**: From {functional_before}% to {functional_after}% of surgical patients with functional vision (6/18 or better)
- **Independence Restored**: {functional_change} percentage point increase in patients able to function independently
- **Quality of Life**: Dramatic shift from predominantly poor vision to good vision among those who received surgery

## Vision Transformation

The Mo Dewji Foundation eye camps demonstrated remarkable success in transforming vision across all time points:

![VA Distribution Area Chart](visualizations/va_distribution_area_chart.png)
*Visual representation of the transformation in vision quality across all follow-up periods*

![VA Distribution by Timepoint](visualizations/va_distribution_by_timepoint.png)
*Comprehensive view of visual acuity improvement across all time points (Pre-Op, 1-Day, 2-Weeks, 1-Month)*

## Overall Visual Acuity Journey - All Eye Camp Surgeries

![VA Journey Cataract](visualizations/va_journey_cataract.png)
*Median visual acuity improvement journey for cataract patients across all eye camp locations, showing all time points*

## Location-Specific Visual Acuity Outcomes

### KIVULE Eye Camp Visual Acuity Journey
![VA Journey KIVULE](visualizations/va_journey_cataract_KIVULE.png)
*Visual acuity improvement for cataract patients at KIVULE eye camp across all time points*

### MASASI Eye Camp Visual Acuity Journey  
![VA Journey MASASI](visualizations/va_journey_cataract_MASASI.png)
*Visual acuity improvement for cataract patients at MASASI eye camp across all time points*

### MWANGA Eye Camp Visual Acuity Journey
![VA Journey MWANGA](visualizations/va_journey_cataract_MWANGA.png)
*Visual acuity improvement for cataract patients at MWANGA eye camp across all time points*

### SIHA Eye Camp Visual Acuity Journey
![VA Journey SIHA](visualizations/va_journey_cataract_SIHA.png)
*Visual acuity improvement for cataract patients at SIHA eye camp across all time points*

## Success Rate Analysis by Demographics

Success rates (achieving 6/18 or better vision) vary across different patient groups:
"""

# Add demographic success tables
gender_success = pd.read_csv('tables/gender_success.csv')
age_success = pd.read_csv('tables/age_success.csv')

content += "\n### Gender-Based Success Rates\n\n"
content += "|| Gender  |   Total_Patients |   Success_Count |   Success_Rate (%) |\n"
content += "||:--------|-----------------:|----------------:|-------------------:|\n"
for _, row in gender_success.iterrows():
    content += f"|| {row['SEX']:<6} |              {int(row['Total_Patients']):>3} |             {int(row['Success_Count']):>3} |               {row['Success_Rate (%)']:>4.1f} |\n"

content += "\n### Age-Based Success Rates\n\n"
content += "|| Age Group  |   Total_Patients |   Success_Count |   Success_Rate (%) |\n"
content += "||:-----------|-----------------:|----------------:|-------------------:|\n"
for _, row in age_success.iterrows():
    content += f"|| {row['Age_Group']:<9} |              {int(row['Total_Patients']):>3} |             {int(row['Success_Count']):>3} |               {row['Success_Rate (%)']:>4.1f} |\n"

content += f"""

## Key Insights and Impact

The Mo Dewji Foundation eye camp surgeries in 2025 demonstrate:

1. **Exceptional Volume**: {total_patients} surgical interventions across four strategic locations
2. **Gender Equity**: Strong representation of female patients ({female_pct:.1f}%) ensuring equal access
3. **Age Appropriateness**: Average age of {avg_age:.1f} years with {age_60_plus_pct:.1f}% of patients aged 60+, targeting high-need elderly population
4. **Geographic Coverage**: Successful outreach to four distinct communities with MASASI serving the largest population
5. **Clinical Excellence**: {functional_after:.1f}% success rate in achieving functional vision
6. **Cataract Focus**: {sics_pct:.1f}% of surgeries addressing cataracts, the leading cause of preventable blindness
7. **Transformative Impact**: {functional_change} percentage point increase in functional vision

The eye camp surgeries represent a significant public health intervention, transforming lives through restored vision and enabling independent daily activities for hundreds of patients across Tanzania.

---

*Report generated for Mo Dewji Foundation Eye Camps Programme 2025 - Surgical Impact Analysis*
"""

# Write the complete updated file
with open('new.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ COMPLETE new.md REGENERATED with ALL CORRECT NUMBERS!")
print(f"📊 Key statistics included:")
print(f"  - Total patients: {total_patients}")
print(f"  - Gender: {female_pct:.1f}% Female ({female_count}), {male_pct:.1f}% Male ({male_count})")
print(f"  - Average age: {avg_age:.1f} years")
print(f"  - SICS: {sics_count} ({sics_pct:.1f}%), Pterygium: {pterygium_count} ({pterygium_pct:.1f}%)")
print(f"  - Vision improvement: {functional_before}% → {functional_after}% (+{functional_change} pp)")
print(f"  - Eye distribution: RE {re_count}, LE {le_count}")
print(f"  - Location distribution: MASASI {masasi_count}, SIHA {siha_count}, KIVULE {kivule_count}, MWANGA {mwanga_count}")
