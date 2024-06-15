#strategy of frequency market bidding

import pandas as pd
import pickle

'''
Input: dataframe with datetime, prissetting [EUR/MW], volume [MW], activation [MW]

Strategy: 
- Sort the dataframe by prissetting
- Choose the 10 highest prissetting hours
- Return a list of datetime with corresponding prissetting [EUR/MW], activation [MW]
'''

#area = 'NO1'
#markets = ['aFRR down']
#year = 2023

def strategy(area='NO1', year=2023, markets='aFRR down', price = 100):

    with open('data_markets/2023_norway.pkl', 'rb') as f:
        data = pickle.load(f)

    df = data[area]
    #remove timezone
    df['Datetime'] = df['Datetime'].dt.tz_localize(None)
    df = df.set_index('Datetime')  # rearange Datetime column to be the index
    df = df.clip(lower=0)  # keep only positive values
    df = df.fillna(0)  # fill nan values with zero

    #create df_spot
    df_spot = df.copy()
    df_mFRR = df.copy()
    df_aFRR = df.copy()

    #keep only the columns with 'NO1 EUR_per_MWh'
    df_spot = df_spot.filter(like='NO1 EUR_per_MWh', axis=1)
    df_mFRR = df_mFRR.filter(like='mFRR EAM down EUR/MWh', axis=1)
    df_aFRR = df_aFRR.filter(like='aFRR down EUR/MW', axis=1)



    matching_columns = [col for col in df.columns if any(market in col for market in markets)]  # Use list comprehension to find matching columns
    #add a 'NO1 EUR_per_MWh' to matching_columns
    matching_columns.append('NO1 EUR_per_MWh')
    matching_columns.append('mFRR EAM down EUR/MWh')



    df = df[matching_columns] # Filter the DataFrame to only include matching columns
    df.to_excel('strategy.xlsx')

    #remove all dates with zero values in column (marked[0] + 'MW v2)
    df = df.loc[(df[markets[0] + ' MW v2'] != 0)]


    #sort the dataframe by prissetting
    df = df.sort_values(by=markets[0] + ' EUR/MW', ascending=False)

    #cut the dataframe on a prissetting
    df = df[df[markets[0] + ' EUR/MW'] > price]

    return df, df_spot, df_mFRR, df_aFRR

#call the function
#df_strategy, df_spot = strategy(area, year, markets, prissetting = 100)
df_strategy, df_spot, df_mFRR, df_aFRR = strategy(area='NO1', year=2023, markets=['aFRR down'], price = 0)



#multiply the columns to get the total cost
df_strategy['marked'] = df_strategy['aFRR down MW v2'] * df_strategy['aFRR down EUR/MW']
#print the sum of the columns
print(df_strategy['aFRR down MW v2'].sum())
print(df_strategy['marked'].sum())

#make excel file

df_aFRR.to_excel('aFRR.xlsx')

#print(df_strategy['aFRR down MW v2'].sum())
#print(df_strategy['aFRR down MW'].sum())
#print(df_strategy['aFRR down MWh activated'].sum())

#print(df_strategy['aFRR down EUR/MW'].mean())
'''
import matplotlib.pyplot as plt
import seaborn as sns

# Setting a style for all plots
#sns.set(style="white")

def plot_dual_y_axis():
    fig, ax1 = plt.subplots(figsize=(12, 6))
    color = 'tab:blue'
    ax1.set_xlabel('Tid (time)', fontsize=14)
    ax1.set_ylabel('Innkjøpt volum (MW)', color=color, fontsize=14)
    ax1.bar(df_strategy.index, df_strategy['aFRR down MW v2'], color=color)
    ax1.tick_params(axis='y', labelcolor=color, labelsize=12)
    ax1.grid(True)

    max_y1 = df_strategy['aFRR down MW v2'].max()

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Aktivert volum (MWh)', color=color, fontsize=14)
    ax2.bar(df_strategy.index, df_strategy['aFRR down MWh activated'], color=color, alpha=0.3)
    ax2.tick_params(axis='y', labelcolor=color, labelsize=12)

    max_y2 = df_strategy['aFRR down MWh activated'].max()
    max_y = max(max_y1, max_y2)
    ax1.set_ylim(0, max_y)
    ax2.set_ylim(0, max_y)
    title = 'Innkjøpt og aktivert volum i aFRR ned for NO1 i 2023'
    ax1.set_title(title, fontsize=16)
    fig.tight_layout()
    plt.savefig('aFRR_down_volume.png')
    plt.show()

def plot_unified_y_axis():
    fig, ax1 = plt.subplots(figsize=(12, 6))
    color_spot = 'darkred'
    ax1.set_xlabel('Tid (time)', fontsize=14)
    ax1.set_ylabel('EUR/MWh', fontsize=14)
    bars1 = ax1.bar(df_spot.index, df_spot['NO1 EUR_per_MWh'], color=color_spot, label='Spotpris')
    color_mfrr = 'darkgreen'
    bars2 = ax1.bar(df_mFRR.index, df_mFRR['mFRR EAM down EUR/MWh'], color=color_mfrr, alpha=0.3, label='mFRR ned pris')
    ax1.legend()
    ax1.tick_params(axis='both', which='major', labelsize=12)
    ax1.grid(True)
    title = 'Spot og mFRR ned priser for NO1 i 2023'
    ax1.set_title(title, fontsize=16)
    fig.tight_layout()
    plt.savefig('spot_mfrr_down_prices.png')
    plt.show()

def plot_simple_bar():
    plt.figure(figsize=(12, 6))
    plt.bar(df_aFRR.index, df_aFRR['aFRR down EUR/MW'], color='navy')
    tittel  = 'aFRR ned priser per MW for NO1 i 2023'
    plt.title(tittel, fontsize=16)
    plt.xlabel('Tid (time)', fontsize=14)
    plt.ylabel('EUR/MW', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('aFRR_down_prices.png')
    plt.show()

# Run the functions to plot
#plot_dual_y_axis()
#plot_unified_y_axis()
#plot_simple_bar()
'''