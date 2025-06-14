import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import os
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Create visualizations directory if it doesn't exist
os.makedirs('visualizations', exist_ok=True)

# Read the data
df = pd.read_csv('operated_eye_va_data.csv')

# Count patients by location
location_counts = df['PATIENTS PHYSICAL ADDRSS '].value_counts()
print("Patient counts by location:")
print(location_counts)

# Create a dataframe with location coordinates
# Note: These are approximate coordinates for demonstration purposes
location_data = {
    'Location': ['MASASI TC', 'KOROGWE TC', 'NACHINGWEA', 'KONDOA DC', 'IFAKARA'],
    'Latitude': [-10.7326, -5.1552, -10.3833, -4.9033, -8.1298],
    'Longitude': [38.8007, 38.4866, 38.7667, 35.7947, 36.6711],
    'Patients': [location_counts.get('MASASI TC', 0),
                location_counts.get('KOROGWE TC', 0),
                location_counts.get('NACHINGWEA', 0),
                location_counts.get('KONDOA DC', 0),
                location_counts.get('IFAKARA', 0)]
}

locations_df = pd.DataFrame(location_data)
print("\nLocation data with coordinates:")
print(locations_df)

try:
    # Try to load Tanzania shapefile
    # If you don't have the shapefile, this will create a simple map without country boundaries
    tanzania = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    tanzania = tanzania[tanzania.name == 'Tanzania']
    
    # Create a figure and axis with Tanzania map
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    tanzania.plot(ax=ax, color='lightgrey', edgecolor='black')
    
    # Plot eye camp locations with size based on number of patients
    plt.scatter(locations_df['Longitude'], locations_df['Latitude'], 
                s=locations_df['Patients']/10, # Scale down for better visualization
                c=locations_df['Patients'],
                cmap='viridis',
                alpha=0.7,
                edgecolors='black',
                linewidths=1)
    
    # Add labels for each location
    for idx, row in locations_df.iterrows():
        plt.annotate(f"{row['Location']}\n({row['Patients']} patients)",
                    (row['Longitude'], row['Latitude']),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=10,
                    fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.7))
    
    plt.title('Eye Camp Locations in Tanzania (2024)', fontsize=16, fontweight='bold')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    
    # Add colorbar
    cbar = plt.colorbar()
    cbar.set_label('Number of Patients', fontsize=12)
    
except Exception as e:
    print(f"Error loading shapefile: {e}")
    print("Creating a simple scatter plot instead...")
    
    # Create a simple scatter plot without country boundaries
    plt.figure(figsize=(12, 10))
    
    # Create a custom colormap
    colors = [(0.8, 0.8, 1), (0, 0, 0.8)]  # Light blue to dark blue
    cm = LinearSegmentedColormap.from_list('custom_cmap', colors, N=100)
    
    # Plot eye camp locations with size based on number of patients
    scatter = plt.scatter(locations_df['Longitude'], locations_df['Latitude'], 
                s=locations_df['Patients'], # Size based on patient count
                c=locations_df['Patients'],
                cmap='viridis',
                alpha=0.7,
                edgecolors='black',
                linewidths=1)
    
    # Add labels for each location
    for idx, row in locations_df.iterrows():
        plt.annotate(f"{row['Location']}\n({row['Patients']} patients)",
                    (row['Longitude'], row['Latitude']),
                    xytext=(15, 15),
                    textcoords='offset points',
                    fontsize=12,
                    fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='black'),
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.7))
    
    plt.title('Eye Camp Locations in Tanzania (2024)', fontsize=16, fontweight='bold')
    plt.xlabel('Longitude', fontsize=14)
    plt.ylabel('Latitude', fontsize=14)
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Number of Patients', fontsize=14)
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)

# Create a simple bar chart of patients by location
plt.figure(figsize=(12, 6))
bars = plt.bar(locations_df['Location'], locations_df['Patients'], color='skyblue', edgecolor='black')

# Add data labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 5,
            f'{int(height)}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Number of Patients by Eye Camp Location', fontsize=16, fontweight='bold')
plt.xlabel('Location', fontsize=14)
plt.ylabel('Number of Patients', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the figures
plt.savefig('visualizations/eye_camp_locations_bar.png', dpi=300, bbox_inches='tight')
print("Bar chart saved to visualizations/eye_camp_locations_bar.png")

plt.tight_layout()
plt.savefig('visualizations/eye_camp_locations_map.png', dpi=300, bbox_inches='tight')
print("Map saved to visualizations/eye_camp_locations_map.png") 