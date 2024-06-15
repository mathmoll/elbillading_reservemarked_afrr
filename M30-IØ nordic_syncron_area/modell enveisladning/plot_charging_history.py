'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Excel file
df = pd.read_excel("/Users/mathiasmollatt/Library/CloudStorage/OneDrive-NorwegianUniversityofLifeSciences/Materielle/01. Mathias/04. metode/M30-IØ nordic_syncron_area/charging_history_df.xlsx", parse_dates=['date'])
df['charge_kW'] = df['charge_MW'] * 1000  # Convert MW to kW

# Create a directory for the plots if it doesn't exist
import os

plots_directory = "car_charging_plots"
os.makedirs(plots_directory, exist_ok=True)

# Iterate over each unique car_name
for car_name in df['car_name'].unique():
    car_df = df[df['car_name'] == car_name]

    # Correcting the approach to identify key dates
    arrival_departure_dates = pd.Index(car_df['date'][car_df['type'].isin(['arrival', 'departure'])])
    type_change_dates = pd.Index(car_df.drop_duplicates('type')['date'])
    key_dates = arrival_departure_dates.union(type_change_dates)

    # Plotting
    plt.figure(figsize=(16, 8))
    colors = car_df['type'].map({'charge_reserve': 'blue', 'charge_spot': 'orange'}).fillna('grey')

    for date, row in car_df.iterrows():
        plt.bar(row['date'], row['charge_kW'], width=0.02, color=colors.loc[date])

    # Mark arrivals and departures
    for arrival in car_df['date'][car_df['type'] == 'arrival']:
        plt.axvline(x=arrival, color='red', linestyle='--', lw=2,
                    label='Arrival' if arrival == car_df['date'][car_df['type'] == 'arrival'].iloc[0] else "")
    for departure in car_df['date'][car_df['type'] == 'departure']:
        plt.axvline(x=departure, color='green', linestyle='--', lw=2,
                    label='Departure' if departure == car_df['date'][car_df['type'] == 'departure'].iloc[0] else "")

    # Formatting the plot
    plt.title(f'Charge Over Time for Car {car_name}')
    plt.xlabel('Date and Time')
    plt.ylabel('Charge (kW)')
    plt.xticks(rotation=45)
    plt.gca().set_xticks(key_dates)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper left')


    plt.tight_layout()

    # Save the plot to a file
    plot_filename = os.path.join(plots_directory, f'{car_name}.png')
    plt.show()
    plt.savefig(plot_filename)
    plt.close()  # Close the plot to free memory

'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Load the Excel file
df = pd.read_excel("/Users/mathiasmollatt/Library/CloudStorage/OneDrive-NorwegianUniversityofLifeSciences/Materielle/01. Mathias/04. metode/M30-IØ nordic_syncron_area/charging_history_df.xlsx", parse_dates=['date'])
df['charge_kW'] = df['charge_MW'] * 1000  # Convert MW to kW

# Create a directory for the plots if it doesn't exist
plots_directory = "car_charging_plots"
os.makedirs(plots_directory, exist_ok=True)

# Iterate over each unique car_name
for car_name in df['car_name'].unique():
    car_df = df[df['car_name'] == car_name]

    # Identifying key dates for x-axis
    arrival_departure_dates = pd.Index(car_df['date'][car_df['type'].isin(['arrival', 'departure'])])
    type_change_dates = pd.Index(car_df.drop_duplicates('type')['date'])
    key_dates = arrival_departure_dates.union(type_change_dates)

    # Plotting
    plt.figure(figsize=(16, 8))
    # Map colors and labels in Norwegian
    color_map = {'charge_reserve': ('blue', 'Aktiveringsladning'), 'charge_spot': ('orange', 'Ladeplan Ladning')}
    car_df['color'] = car_df['type'].map(lambda x: color_map[x][0] if x in color_map else 'grey')
    car_df['label'] = car_df['type'].map(lambda x: color_map[x][1] if x in color_map else '')

    seen_labels = set()
    for (date, row) in car_df.iterrows():
        label = row['label'] if row['label'] not in seen_labels and row['label'] != '' else ""
        plt.bar(row['date'], row['charge_kW'], width=0.02, color=row['color'], label=label)
        if label:
            seen_labels.add(row['label'])

    # Mark arrivals and departures
    for arrival in car_df['date'][car_df['type'] == 'arrival']:
        plt.axvline(x=arrival, color='red', linestyle='--', lw=2,
                    label='Ankomst' if 'Ankomst' not in seen_labels else "")
        seen_labels.add('Ankomst')
    for departure in car_df['date'][car_df['type'] == 'departure']:
        plt.axvline(x=departure, color='green', linestyle='--', lw=2,
                    label='Avgang' if 'Avgang' not in seen_labels else "")
        seen_labels.add('Avgang')

    # Formatting the plot
    plt.title(f'Ladehistorikk for ID: {car_name}')
    plt.xlabel('Hendelseslogg for ladning')
    plt.ylabel('Ladning (kWh/h)')
    plt.xticks(rotation=45)
    plt.gca().set_xticks(key_dates)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))

    # Ensure legend is not repeated
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper left')

    plt.tight_layout()

    # Save the plot to a file
    plot_filename = os.path.join(plots_directory, f'{car_name}.png')
    plt.savefig(plot_filename)
    plt.close()  # Close the plot to free memory
