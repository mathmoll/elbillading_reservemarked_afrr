    from data_gp_filtering_preprocess import create_schedule_from_zaptec_csv
    from datetime import datetime
    from simulation1 import Simulation
    import pandas as pd
    import numpy as np  # Make sure to import numpy

    schedule = {
        'car1': {'arrivals': [datetime(2023, 1, 1, 0)],
                 'departures': [datetime(2023, 12, 31, 23)],
                 'specs': {'battery_MWh': 10, 'discharge_MW': 0, 'charge_MW': 1, 'SOC_MWh': 0}},
        'car2': {'arrivals': [datetime(2023, 1, 2, 0)],
                 'departures': [datetime(2023, 12, 31, 23)],
                 'specs': {'battery_MWh': 10, 'discharge_MW': 0, 'charge_MW': 1, 'SOC_MWh': 0}},
        'car3': {'arrivals': [datetime(2023, 1, 3, 0)],
                    'departures': [datetime(2023, 8, 31, 23)],
                    'specs': {'battery_MWh': 10, 'discharge_MW': 0, 'charge_MW': 1, 'SOC_MWh': 0}},
    }

    schedule = create_schedule_from_zaptec_csv('data_gp/gp_zaptec_detailed.csv')
    #schedule = create_schedule_from_zaptec_csv('data_gp/duplicated_zaptec_data.csv')
    senario = 'departure'
    maks = 0.436


    #andel_verdier = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]  # Specific values for andel
    andel_verdier = [1]
    minste_bud_volum_verdier = [0.001]  # Specific values for min_bud

    price_low = 15
    price_high = 19
    price_step = 5

    summary = {}
    for minste_bud_volum in minste_bud_volum_verdier:
        for andel in andel_verdier:
            for prissetting in range(price_low, price_high, price_step):
                sim = Simulation(schedule, parkinglot_capacity=300, scenario=senario, clearing_price=prissetting, markets=['aFRR down'], min_bid=minste_bud_volum, andel=andel, max_bud=maks, granularity=True)
                sim.run()
                df = sim.to_dataframe()  # Get the simulation results as a DataFrame
                charging_history_df = sim.get_charging_history_dataframe()  # Get the charging history as a DataFrame

                summary_key = f'andel_{andel}_min_bud_{minste_bud_volum}_price_{prissetting}'
                summary[summary_key] = {
                    'Andel': andel,
                    'Minste bud volum': minste_bud_volum,
                    'Prissetting': prissetting,
                    'sum_spot_charge': df['spot_charge_MW'].sum(),
                    'sum_activation_charge': df['reserve_charge_MW'].sum(),
                    'total_volume': df['spot_charge_MW'].sum() + df['reserve_charge_MW'].sum(),
                    'sum_failed_bids': df['warning'].sum(),
                    'sum_rev_spot': df['revenue_spot'].sum(),
                    'sum_rev_bids': df['revenue_reserve'].sum(),
                    'sum_rev_comp': df['revenue_comp_reserve'].sum(),
                    'sum_rev': df['revenue_spot'].sum() + df['revenue_reserve'].sum() + df['revenue_comp_reserve'].sum()
                }
                print(summary[summary_key])

    df_summary = pd.DataFrame.from_dict(summary, orient='index')

    #df_summary.to_excel('summary_results.xlsx')  # Export summary results to an Excel file
    charging_history_df.to_excel('charging_history_df.xlsx') #make a excel file of charging_history_df
    df.to_excel('df.xlsx') #make a excel file of data
