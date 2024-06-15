from datetime import datetime, timedelta
from parkinglot1 import ParkingLot
from car1 import Car
from strategy1 import strategy
from bid1 import bid
from bid_car import bid_car
import pandas as pd


class Simulation:
    def __init__(self, schedule, parkinglot_capacity, scenario, clearing_price, markets, min_bid, andel, max_bud, granularity=None):
        self.schedule = schedule
        self.parking_lot = ParkingLot(parkinglot_capacity)
        self.clearing_price = clearing_price
        self.markets = markets
        self.all_cars = {}  # Store all cars ever added to the simulation
        self.start_date = datetime(2023, 1, 1)
        self.end_date = datetime(2023, 12, 31, 23)
        self.aggregated_data = []
        self.scenario = scenario
        self.min_bid = min_bid
        self.andel = andel
        self.granularity = granularity
        self.max_bud = max_bud
    def run(self):
        df_strategy, df_spot, df_mFRR, df_aFRR = strategy(area='NO1', year=2023, markets=self.markets, price=self.clearing_price)

        current_date = self.start_date
        while current_date <= self.end_date:

            # Initialize variables for this hour
            spot_charge_MW = 0
            #spot_discharge_MW = 0
            total_SOC_MWh = 0
            reserve_charge_MW = 0
            car_arrival = 0
            car_departure = 0


            # Check and manage arrivals and departures
            for car_name, car_info in self.schedule.items():
                if current_date in car_info['arrivals']:
                    if car_name not in self.all_cars:  # If car is new, create and add to all_cars
                        new_car = Car(car_name, **car_info['specs'])
                        self.all_cars[car_name] = new_car
                        car_arrival += 1
                    self.parking_lot.add_car(self.all_cars[car_name], car_info['departures'])  # Add car to parking lot
                    self.all_cars[car_name].append_arrival(current_date)  # Append arrival to car's history



            # Charge cars based on scenario
            if self.scenario == "arrival":
                for car_name, car in self.parking_lot.parked_cars.items():
                    car.status = None  # Reset car status
                    if car.SOC_MWh < car.battery_MWh:  # If car is not fully charged
                        car.status = 'spot_charging'  # Update car status
                        charge_added = car.charge(1, current_date)  # Charge for 1 hour or simulation tick
                        spot_charge_MW += charge_added  # Update total charge
                    total_SOC_MWh += car.SOC_MWh  # Aggregate SOC of all cars

            if self.scenario == "departure":
                for car_name, car in self.parking_lot.parked_cars.items():
                    car.status = None
                    if car.SOC_MWh < car.battery_MWh:  # If car is not fully charged
                        time_to_charge = car.time_to_full_charge()
                        charge_start_time = car.departure_time[0] - timedelta(hours=time_to_charge)

                        charge_start_time = charge_start_time.replace(minute=0, second=0, microsecond=0)
                        if current_date >= charge_start_time:
                            #print(f"Car {car_name} is charging.", car.departure_time, charge_start_time, current_date)
                            car.status = 'spot_charging'
                            charge_added = car.charge(1, current_date)
                            spot_charge_MW += charge_added
                    total_SOC_MWh += car.SOC_MWh  # Aggregate SOC of all cars

            num_cars = len(self.parking_lot.parked_cars) # Count the number of cars in the parking lot
            total_battery_MWh = sum([car.battery_MWh for car in self.parking_lot.parked_cars.values()]) # Calculate total battery capacity
            agg2_bid_energy_MWh = total_battery_MWh - total_SOC_MWh # Calculate total energy available for bidding

            charge_MW = sum([car.charge_MW for car in self.parking_lot.parked_cars.values()]) # Calculate total charge rate of all cars
            agg2_bid_charge_MW = charge_MW - spot_charge_MW # calculate aggretated bid charge rate

            discharge_MW = sum([car.discharge_MW for car in self.parking_lot.parked_cars.values()])  # Calculate total discharge rate of all cars
            agg_bid_discharge_MW = discharge_MW  # calculate aggretated bid discharge rate

            columns = []
            for i in df_strategy.columns:
                columns.append(i)  # save i into a list
            type_marked = str(columns[0][0:9])

            if current_date in df_spot.index:
                spot_price = -float(df_spot.loc[current_date].iloc[0])
                mFRR_price = float(df_mFRR.loc[current_date].iloc[0])
                aFRR_price_all = float(df_aFRR.loc[current_date].iloc[0])


            # Calculate total charge rate of all cars with car.status = None
            agg_bid_charge_MW = 0
            agg_bid_energy_MWh = 0
            for car_name, car in self.parking_lot.parked_cars.items():
                if car.SOC_MWh < car.battery_MWh and car.status == None:
                    car_bid = bid_car((car.battery_MWh - car.SOC_MWh), car.discharge_MW, car.charge_MW, type_marked)
                    agg_bid_charge_MW += car_bid
                    agg_bid_energy_MWh += car_bid
                    #print(car_name, agg2_bid_energy_MWh, agg2_bid_charge_MW)

            #print(current_date, agg2_bid_charge_MW, agg2_bid_energy_MWh)



            if current_date in df_strategy.index:
                marked_price = df_strategy.loc[current_date][0]
                marked_volume1 = df_strategy.loc[current_date][1]
                marked_volume2 = df_strategy.loc[current_date][2]
                activation = df_strategy.loc[current_date][3]
                #spot_price = df_strategy.loc[current_date][4]
                #mFRR_price = df_strategy.loc[current_date][5]
                bidding = bid(agg_bid_energy_MWh, agg_bid_discharge_MW, agg_bid_charge_MW, type_marked, self.min_bid, self.andel, self.max_bud, self.granularity)

            else:
                marked_price = 0
                marked_volume1 = 0
                marked_volume2 = 0
                #mFRR_price = 0
                activation = 0
                bidding = 0


            warning = 0

            if bidding != 0:
                activation_share_MWh = (bidding / marked_volume2) * activation
                if agg_bid_energy_MWh > activation_share_MWh:
                    self.parking_lot.parked_cars = dict(sorted(self.parking_lot.parked_cars.items(), key=lambda x: x[1].departure_time))
                    amount = activation_share_MWh
                    for car_name, car in self.parking_lot.parked_cars.items():
                        if car.status == None:
                            if amount >= 0:
                                if car.SOC_MWh < car.battery_MWh:
                                    car.status = 'reserve_charging'
                                    reserve_charge_added = car.charge(1, current_date, amount)
                                    amount -= reserve_charge_added
                                    reserve_charge_MW += reserve_charge_added
                        else:
                            amount -= 0
                            reserve_charge_MW += 0
                    if amount > 0: # if there is no car available for reserve charging, bidding is not possible
                        #print('Warning: Not enough cars available for reserve charging')
                        #print nicer format
                        #print(current_date, bidding, activation_share_MWh, amount)
                        warning = 1
                        #bidding = 0
            else:
                activation_share_MWh = 0
                reserve_charge_MW = 0
                bidding = 0

            if -spot_price < mFRR_price:
                mFRR_price = -spot_price

            diff_mFRR_spot = -mFRR_price


            if marked_volume2 == 0:
                bidding = 0

            if total_battery_MWh > 0:
                SOC = total_SOC_MWh / total_battery_MWh * 100
            else:
                SOC = 0


            if bidding != 0:
                diff_bidding = (bidding * 1/self.andel) - bidding
            else:
                diff_bidding = 0


            for car_name, car_info in self.schedule.items():
                if current_date in car_info['departures']:
                    self.parking_lot.remove_car(car_name)  # Remove car from parking lot
                    car_departure += 1
                    self.all_cars[car_name].append_departure(current_date)  # Append departure to car's history


            # Append aggregated data for this hour
            self.aggregated_data.append({
                'timestamp': current_date,
                'min_bid': self.min_bid,
                'andel': self.andel,
                'clearing_price': self.clearing_price,
                'num_cars': num_cars,
                'car_arrival': car_arrival,
                'car_departure': car_departure,
                'energy_MWh': total_battery_MWh,
                'SOC_MWh': total_SOC_MWh,
                #'SOC %': SOC,
                'charge_MW': charge_MW,
                #'discharge_MW': discharge_MW,
                'spot_charge_MW': spot_charge_MW,
                #'spot_discharge_MW': 0,
                'reserve_charge_MW': reserve_charge_MW,
                #'reserve_discharge_MW': 0,
                'agg_bid_energy_MWh': agg_bid_energy_MWh,
                'agg_bid_charge_MW': agg_bid_charge_MW,
                #'agg2_bid_charge_MW': agg2_bid_charge_MW,
                #'agg2_bid_energy_MWh': agg2_bid_energy_MWh,
                #'agg_bid_discharge_MW': 0,
                'bidding': bidding,
                'no_bid': agg_bid_energy_MWh,
                'diff_bidding': diff_bidding,
                'activation_share_MWh': activation_share_MWh,
                'test': activation_share_MWh-reserve_charge_MW,
                'warning': warning,
                columns[0]: marked_price,
                columns[1] : marked_volume1,
                columns[2]: marked_volume2,
                columns[3]: activation,
                'mFRR EAM down EUR/MWh': mFRR_price,
                'spot_price': spot_price,
                'diff_mFRR_spot': diff_mFRR_spot,
                'aFRR down EUR/MW_all': aFRR_price_all,
                'revenue_reserve': (bidding * marked_price),
                'revenue_comp_reserve' : reserve_charge_MW * diff_mFRR_spot,
                'revenue_spot' : float(spot_charge_MW * spot_price),
                'rev_total': (float(spot_charge_MW * spot_price) + (bidding * marked_price) + (reserve_charge_MW * diff_mFRR_spot))
            })



            current_date += timedelta(hours=1)  # Move to the next simulation tick


    def to_dataframe(self):
        return pd.DataFrame(self.aggregated_data)

    def get_charging_history_dataframe(self):
        all_charging_records = []

        for car_name, car in self.all_cars.items():
            for record in car.charging_history:
                # Ensure that each record now includes 'charge_MW' and 'discharge_MW' along with the other data
                all_charging_records.append({
                    'car_name': car_name,
                    'date': record['date'],
                    'SOC_MWh': record['SOC_MWh'],
                    'type': record['type'],
                    'charge_MW': record['charge_MW'],
                    'discharge_MW': record.get('discharge_MW', 0),
                    'battery_MWh': record['battery_MWh']
                })

        charging_history_df = pd.DataFrame(all_charging_records)
        return charging_history_df


