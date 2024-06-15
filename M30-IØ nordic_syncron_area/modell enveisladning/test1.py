import pandas as pd


def check_multiple_charges_per_hour(file_path):
    # Load the data from the Excel file
    data = pd.read_excel(file_path)

    # Convert 'date' to datetime to ensure proper grouping
    data['date'] = pd.to_datetime(data['date'])

    # Group by car_name, date (including hour), and type, then count occurrences
    grouped_data = data.groupby(['car_name', data['date'].dt.floor('H'), 'type']).size()

    # Find instances where a car has more than one charging session of the same type in the same hour
    multiple_sessions = grouped_data[grouped_data > 1].reset_index(name='count')

    # Check if there are any cars with multiple charging sessions in the same hour
    if multiple_sessions.empty:
        print("No cars were charged multiple times within the same hour.")
    else:
        print("Cars with multiple charging sessions within the same hour:")
        for index, row in multiple_sessions.iterrows():
            print(
                f"Car ID: {row['car_name']}, Date and Hour: {row['date']}, Charge Type: {row['type']}, Count: {row['count']}")

def check_if_cars_are_fully_charged_at_departure(file_path):
    # Load the data from the Excel file
    data = pd.read_excel(file_path)

    # Filter data to include only departure events
    departures = data[data['type'] == 'departure']

    # Check if any cars are not fully charged at departure
    not_fully_charged = departures[departures['SOC_MWh'] < departures['battery_MWh']]

    # Check if there are any cars that are not fully charged at departure
    if not_fully_charged.empty:
        print("All cars were fully charged at departure.")
    else:
        print("Cars not fully charged at departure:")
        for index, row in not_fully_charged.iterrows():
            car_data = data[data['car_name'] == row['car_name']]
            parked_hours = (car_data['date'].max() - car_data['date'].min()).total_seconds() / 3600
            print(f"Car ID: {row['car_name']}, Departure Date: {row['date']}, SOC: {row['SOC_MWh']} / {row['battery_MWh']} MWh, Parked Hours: {parked_hours}")

def show_charging_history_for_car(filepath, car_name):
    # Filter data to include only charging history for the specified car
    data = pd.read_excel(file_path)
    car_data = data[data['car_name'] == car_name]

    # Display the charging history for the car
    print(f"Charging history for car {car_name}:")
    #print(car_data)
    return car_data


if __name__ == "__main__":
    file_path = '/Users/mathiasmollatt/Library/CloudStorage/OneDrive-NorwegianUniversityofLifeSciences/Materielle/01. Mathias/04. metode/M30-IØ nordic_syncron_area/charging_history_df.xlsx'  # Change this to your Excel file path
    check_multiple_charges_per_hour(file_path)
    check_if_cars_are_fully_charged_at_departure(file_path)
    car_data = show_charging_history_for_car(file_path,'f2561640-7e76-4e65-b2a8-09a41e251729')  # Change this to the car name you want to inspect
