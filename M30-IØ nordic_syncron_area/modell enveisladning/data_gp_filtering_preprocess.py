import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def gp_charging_stations(csv_file_path):
    df = pd.read_csv(csv_file_path)
    # Load the CSV file into a DataFrame

    # Convert 'rounded_datetime' to datetime format for accurate manipulation
    df['rounded_datetime'] = pd.to_datetime(df['rounded_datetime'])

    # Grouping by 'charge_cycle_id' to compute required values
    result_adjusted = df.groupby('charge_cycle_id').agg(
        id=('charge_cycle_id', 'first'),  # Just replicate the ID
        start_date=('rounded_datetime', 'min'),
        end_date=('rounded_datetime', 'max'),
        min_charge=('Charged_energy', 'min'),  # Find minimum charge value
        energy=('Charged_energy', 'sum')
    ).reset_index(drop=True)

    # invert values in 'energy' column annd min_charge column
    result_adjusted['energy'] = -result_adjusted['energy']
    result_adjusted['min_charge'] = -result_adjusted['min_charge']
    # adjust values from kW to MW
    result_adjusted['energy'] = result_adjusted['energy'] / 1000
    result_adjusted['min_charge'] = result_adjusted['min_charge'] / 1000

    #rounded_datetime to tz-naive
    result_adjusted['start_date'] = result_adjusted['start_date'].dt.tz_localize(None)
    result_adjusted['end_date'] = result_adjusted['end_date'].dt.tz_localize(None)

    # rename columns
    result_adjusted = result_adjusted.rename(columns={'id': 'Kjennemerke',
                                                      'start_date': 'Kamera inn-tid',
                                                        'end_date': 'Kamera ut-tid',
                                                      'energy': 'battery_MWh',
                                                      'min_charge': 'charge_MW'})

    # Calculate the parking duration in hours and add it as a new column
    result_adjusted['Parked Hours'] = (result_adjusted['Kamera ut-tid'] - result_adjusted[
        'Kamera inn-tid']).dt.total_seconds() / 3600

    # remove rows with 'Parked Hours' less than 12
    result_adjusted = result_adjusted[result_adjusted['Parked Hours'] > 12]

    return result_adjusted

def create_schedule_from_zaptec_csv(file_path, default_specs=None):


    # Read the CSV file with specific columns
    #data = pd.read_csv(file_path, usecols=['Id', 'StartDateTime', 'EndDateTime', 'Energy', 'max_power', 'DeviceName'])
    df = pd.read_csv(file_path, usecols=['charge_cycle_id', 'StartDateTime', 'EndDateTime', 'Energy', 'Max_power [kW]'])

    # Rename columns and convert 'Energy' and 'max_power' from kWh to MWh by dividing by 1000
    #df_renamed = data.rename(columns={'Id': 'Kjennemerke', 'Energy': 'battery_MWh', 'max_power': 'charge_MW'})
    df_renamed = df.rename(columns={'charge_cycle_id': 'Kjennemerke', 'Energy': 'battery_MWh', 'Max_power [kW]': 'charge_MW'})
    df_renamed['battery_MWh'] = df_renamed['battery_MWh'] / 1000
    df_renamed['battery_MWh'] = df_renamed['battery_MWh'].round(4)
    df_renamed['charge_MW'] = df_renamed['charge_MW'] / 1000

    # Calculate the parking duration in hours and add it as a new column
    df_renamed['Parked Hours'] = (pd.to_datetime(df_renamed['EndDateTime']) - pd.to_datetime(df_renamed['StartDateTime'])).dt.total_seconds() / 3600

    #calculate the parked days
    df_renamed['Parked Days'] = (pd.to_datetime(df_renamed['EndDateTime']) - pd.to_datetime(df_renamed['StartDateTime'])).dt.days

    # remove rows with 'Parked Hours' less than 12
    #df_renamed = df_renamed[df_renamed['Parked Hours'] > 12]

    # new column with battery_kWh and charge_kW
    df_renamed['battery_kWh'] = df_renamed['battery_MWh'] * 1000
    df_renamed['charge_kW'] = df_renamed['charge_MW'] * 1000

    histogram_parked_hours(df_renamed)
    histogram_ladehastighet(df_renamed)
    historgram_lademengde(df_renamed)

    # Set default specs if not provided
    if default_specs is None:
        print('default_specs is None')
        default_specs = {'battery_MWh': 0.077, 'discharge_MW': 0, 'charge_MW': 0.05, 'SOC_MWh': 0}

    schedule = {}
    for _, row in df_renamed.iterrows():
        car_id = row['Kjennemerke']
        arrival_time = datetime.fromisoformat(str(row['StartDateTime']))
        departure_time = datetime.fromisoformat(str(row['EndDateTime']))
        #print(departure_time)
        #if departure_time in 2024, change datetime to last hour in 2023
        if departure_time.year == 2024:
            departure_time = datetime(2023, 12, 31, 23)
            #print('yes')

        car_specs = default_specs.copy()
        car_specs['charge_MW'] = row['charge_MW']
        car_specs['battery_MWh'] = row['battery_MWh']
        car_specs['SOC_MWh'] = 0

        if car_id not in schedule:
            schedule[car_id] = {
                'arrivals': [arrival_time],
                'departures': [departure_time],
                'specs': car_specs
            }
        else:
            schedule[car_id]['arrivals'].append(arrival_time)
            schedule[car_id]['departures'].append(departure_time)

    return schedule


def histogram_parked_hours(filtered_df):
    # Plot a histogram of the 'Parked Hours' with smaller bins for more detailed distribution
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_df['Parked Days'], bins=25, color='blue', edgecolor='black')  # Increased number of bins for finer granularity
    #adjust automatically the x-axis to fit the data
    plt.title('Histogram parkeringslengde')
    plt.xlabel('Parkeringslengde (dager)')
    plt.ylabel('Frekvens')

    # Show the plot
    plt.show()

def histogram_ladehastighet(filtered_df):
    # Plot a histogram of the 'charge_kW' with smaller bins for more detailed distribution
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_df['charge_kW'], bins=40, color='blue', edgecolor='black')  # Increased number of bins for finer granularity
    #adjust automatically the x-axis to fit the data
    plt.title('Histogram ladehastighet')
    plt.xlabel('Ladehastighet (kW)')
    plt.ylabel('Frekvens')

    # Show the plot
    plt.show()

def historgram_lademengde(filtered_df):
    # Plot a histogram of the 'battery_kWh' with smaller bins for more detailed distribution
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_df['battery_kWh'], bins=25, color='blue', edgecolor='black')  # Increased number of bins for finer granularity
    #adjust automatically the x-axis to fit the data
    plt.title('Histogram lademengde')
    plt.xlabel('Lademengde (kWh)')
    plt.ylabel('Frekvens')

    # Show the plot
    plt.show()

# Usage example:
#file_path = 'data_gp/gp_zaptec_detailed.csv'  # Update this to your actual file path
#schedule = create_schedule_from_zaptec_csv('data_gp/gp_zaptec_detailed.csv')

# Print an example entry from the schedule
#first_key = next(iter(schedule))
#print({first_key: schedule[first_key]})



