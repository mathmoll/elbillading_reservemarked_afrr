from datetime import datetime
class Car:
    def __init__(self, name, battery_MWh, discharge_MW, charge_MW, SOC_MWh = 0):
        self.name = name
        self.battery_MWh = battery_MWh
        self.discharge_MW = discharge_MW
        self.charge_MW = charge_MW
        self.SOC_MWh = SOC_MWh
        self.charging_history = []  # Initialize an empty list to store charging history
        self.arrival_time = None
        self.departure_time = None
        self.status = None



    def charge(self, hours, timestamp, amount_activation = None):
        '''
        # Record the initial SOC before charging
        initial_SOC = self.SOC_MWh

        # SOC-dependent charging logic
        soc_percentage = self.SOC_MWh / self.battery_MWh
        if soc_percentage < 0.25:
            effective_charge_rate = self.charge_MW
        elif soc_percentage < 0.75:
            effective_charge_rate = self.charge_MW * 0.75
        else:
            effective_charge_rate = self.charge_MW * 0.5
        '''
        '''
        if self.departure_time:  # Check if the list is not empty
            # Assuming the first element is the one you're interested in
            first_departure_time = self.departure_time[0]
            #appen to history

        else:
            print("self.departure_time list is empty.")
            #set departure time to last day of the year
            first_departure_time = datetime(2023, 12, 31, 20 )
        '''
        first_departure_time = self.departure_time[0]
        # Check if the car can be charged
        if not first_departure_time == timestamp:
            effective_charge_rate = self.charge_MW
            potential_charge = effective_charge_rate * hours
            if self.status == 'spot_charging': # Update car status
                space_left = self.battery_MWh - self.SOC_MWh
                actual_charge = min(potential_charge, space_left)
                self.SOC_MWh += actual_charge
                self.charging_history.append(
                    {'date': (timestamp),
                     'SOC_MWh': self.SOC_MWh,
                     'type': 'charge_spot',
                     'charge_MW': actual_charge,
                     'battery_MWh': self.battery_MWh})
            elif self.status == 'reserve_charging':  # Update car status
                space_left = self.battery_MWh - self.SOC_MWh
                actual_charge = min(potential_charge, amount_activation, space_left)
                self.SOC_MWh += actual_charge
                self.charging_history.append(
                    {'date': (timestamp),
                     'SOC_MWh': self.SOC_MWh,
                     'type': 'charge_reserve',
                     'charge_MW': actual_charge,
                     'battery_MWh': self.battery_MWh})
            return actual_charge
        else:
            #print('Car can not be charged, due to the departure time')
            actual_charge = 0
            '''
            self.charging_history.append(
                {'date': (timestamp),
                 'SOC_MWh': self.SOC_MWh,
                 'type': 'departure',
                 'charge_MW': actual_charge,
                 'battery_MWh': self.battery_MWh})
            '''
            return actual_charge

    def time_to_full_charge(self):
        """Calculate the time needed to fully charge the car in hours."""
        charge_needed_MWh = self.battery_MWh - self.SOC_MWh
        if self.charge_MW > 0:
            return (charge_needed_MWh / self.charge_MW) + 1  # Add 1 to account for rest charge
        return float('inf')  # Return a large number if charge rate is 0 to indicate it can't be charged

    def append_arrival(self, timestamp):
        """Append an arrival event to the charging history with placeholders for charge and discharge."""
        self.charging_history.append({
            'date': timestamp,
            'type': 'arrival',
            'is_arrival': True,
            'charge_MW': 0,  # Placeholder for arrival, no charging happening yet
            'discharge_MW': 0,  # Placeholder for arrival, no discharging happening
            'SOC_MWh': self.SOC_MWh,  # Current state of charge
            'battery_MWh': self.battery_MWh
        })

    def append_departure(self, timestamp):
        """Append a departure event to the charging history with placeholders for charge and discharge."""
        self.charging_history.append({
            'date': timestamp,
            'type': 'departure',
            'is_departure': True,
            'charge_MW': 0,  # Placeholder for departure, no charging happening
            'discharge_MW': 0,  # Placeholder for departure, no discharging happening
            'SOC_MWh': self.SOC_MWh,  # Current state of charge
            'battery_MWh': self.battery_MWh
        })