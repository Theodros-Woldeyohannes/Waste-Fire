import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams.update({'font.size': 10})

# Folder containing CSV files (change as needed)
folder_path = r'C:\Users\jacks\Documents\UNM\P50\LandFill_Recycle_FireStudy\Journal Submission\Waste-Fire\PM_data_analysis'

# List to store PM2.5 data and corresponding site names for all files
all_pm25_data = []
site_names = []
time_stamps = []

# Dictionary to map site names to fire-report, city, and state code
site_info = {
    'Albuquerque - Site A': 'FR - 1 - Albuquerque - Site A - NM',
    'Casper': 'FR - 2 - Casper - WY',
    'C2 - Site C': 'FR - 3 - C2 - Site C - TX',
    'Dundas': 'FR - 4 - Dundas - MN',
    'Houston': 'FR - 5 - Houston - TX',
    'Las Cruces - Site B': 'FR - 6 - Las Cruces - Site B - NM',
    'Richmond': 'FR - 7 - Richmond - CA',
    'Rio Rancho - Site A': 'FR - 8 - Rio Rancho - Site A - NM',
    'Roseburg': 'FR - 9 - Roseburg - OR',
    'Simi': 'FR - 10 - Simi - CA',
    # Add more mappings as needed
}

# Sites to highlight
highlight_sites = [
    'Roseburg', 'Las Cruces - Site B', 'Richmond', 'Rio Rancho - Site A',
    'C2 - Site C', 'Houston', 'Casper', 'Simi', 'Dundas', 'Albuquerque - Site A', 'Phoenix', 'Bend', 
    'Oakland', 'St. Clair', 'Wellford', 'Pitt Co.', 'Raleigh', 'Albuquerque - Site B', 'Glendale'
]

# Function to detect PM2.5 spikes
def detect_pm_spikes(pm_data, threshold=35):
    spikes = (pm_data > threshold)
    return spikes

# Recursively search for CSV files in all subfolders
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith('.csv'):
            file_path = os.path.join(root, file_name)

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Convert timestamp to datetime
            df['time_stamp_UTC'] = pd.to_datetime(df['time_stamp'], unit='s')

            # Check if 'pm2.5_atm' column exists and if data is not empty
            if 'pm2.5_atm' in df.columns and not df['pm2.5_atm'].empty:
                # Extract PM2.5 data and time stamps
                pm25_data = df['pm2.5_atm']
                time_data = df['time_stamp_UTC']
                site_name = file_name[:-4]  # Extract site name

                # Append PM2.5 data, time data, and site name to the lists
                all_pm25_data.append(pm25_data)
                time_stamps.append(time_data)
                site_names.append(site_name)

# Create a single figure with subplots
num_plots = len(all_pm25_data)
num_cols = 3  # Number of columns
num_rows = -(-num_plots // num_cols)  # Calculate number of rows (ceiling division)

# Create subplots with reduced size
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 4 * num_rows))

# Flatten axes if num_rows > 1
axes = axes.flatten() if num_rows > 1 else [axes]

# Plot each PM2.5 concentration data with site name as label
for ax, pm25_data, time_data, site_name in zip(axes, all_pm25_data, time_stamps, site_names):
    ax.plot(time_data, pm25_data)
    ax.set_xlabel('Time (Date and Hour)')
    ax.set_ylabel('PM2.5 (ug/m^3)')

    # Set x-axis major locator and formatter for better readability
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to show only hours and minutes
    plt.setp(ax.get_xticklabels(), rotation=0, ha='center', fontsize=9)
    # Set the font size smaller and keep it close to the x-axis
    # plt.setp(ax.get_xticklabels(), rotation=0, ha='center', fontsize=4)

    # Highlight certain sites based on specified sites list
    if any(site in site_name for site in highlight_sites):
        ax.set_facecolor('yellow')
    else:
        ax.set_facecolor('white')  # Set non-highlighted sites back to white

    # Update chart names
    if site_name in site_info:
        chart_name = site_info[site_name]
    else:
        chart_name = site_name  # Fallback in case site_name is not in the dictionary

    ax.legend([chart_name])
    ax.grid(True)

# Remove empty subplots
for i in range(num_plots, num_rows * num_cols):
    fig.delaxes(axes[i])

# Adjust layout
plt.tight_layout()
plt.show()
