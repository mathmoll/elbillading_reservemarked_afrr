
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'df.xlsx'
data = pd.read_excel(file_path)

tidslinje = pd.read_excel('tidslinje.xlsx')

#change columna names from Hour to timestamp
tidslinje.rename(columns={'Hour': 'timestamp'}, inplace=True)

#merge data and tidslinje
data = data.merge(tidslinje, how='left', on='timestamp')

#realcost
data['total_charged_energy'] = (data['total_charged_energy']/1000)
data['total_energy_cost'] = data['total_charged_energy'] * data['spot_price']

senario_name = 'basis'
senario_andel = int(data['andel'].iloc[0]*100)
senario_price = int(data['clearing_price'].iloc[0])

predefined_yaxis_EUR_high = max(data['revenue_spot'].max(), data['revenue_reserve'].max(), data['revenue_comp_reserve'].max(), data['total_energy_cost'].max()) + 5
predefined_yaxis_EUR_low = min(data['revenue_spot'].min(), data['revenue_reserve'].min(), data['revenue_comp_reserve'].min(), data['total_energy_cost'].min()) - 5

predefined_yaxis_MW_high = max(data['spot_charge_MW'].max(), data['reserve_charge_MW'].max()) + 0.2
predefined_yaxis_MW_low = 0

predefined_yaxis_EUR_MWh_high = max(data['aFRR down EUR/MW_all'].max(), data['diff_mFRR_spot'].max()) + 5


#Plot1: Spot Charge Plot
plt.figure(figsize=(10, 6))
plt.bar(data['timestamp'], data['spot_charge_MW'], color='blue')
plt.xlabel('Tid (time)')
plt.ylabel('MWh')
plt.title(f'Ladning ved spot (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.xticks(rotation=45)
plt.ylim(0, predefined_yaxis_MW_high)
plt.tight_layout()
plt.savefig('plot1_spot_charge.png')
plt.show()

#Plot2: Spot Price Plot
data['spot_price'] = pd.to_numeric(data['spot_price'], errors='coerce')
plt.figure(figsize=(10, 6))
plt.bar(data['timestamp'], data['spot_price'], color='blue')
plt.xlabel('Tid (time)')
plt.ylabel('EUR/MWh')
plt.title(f'Spot Pris (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.xticks(rotation=45)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('plot2_spot_price.png')
plt.show()

#Plot3: Spot Income Plot
plt.figure(figsize=(10, 6))
plt.bar(data['timestamp'], data['revenue_spot'], color='blue')
plt.xlabel('Tid (time)')
plt.ylabel('EUR')
plt.title(f'Kostnader ved spotladning (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.xticks(rotation=45)
plt.ylim(predefined_yaxis_EUR_low, predefined_yaxis_EUR_high)
plt.tight_layout()
plt.savefig('plot3_spot_income.png')
plt.show()

#Plot4: Bid Volume Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(data['timestamp'], data['no_bid'], color='grey', alpha=0.3, label='Tilgjengelig bud')
ax.bar(data['timestamp'], data['bidding'], color='blue', label='Aksepterte bud')
#ax.bar(data['timestamp'], data['diff_bidding'], bottom=data['bidding'], color='blue', alpha=0.1, label='Tilsidesatt andel')
ax.axhline(y=senario_andel, color='red', linestyle='--', label='Prissettingsnivå')
plt.xlabel('Tid (time)')
plt.ylabel('MW')
plt.title(f'Bud volum (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.xticks(rotation=45)
plt.ylim(0, data['no_bid'].max() + 0.2)
plt.legend()
plt.tight_layout()
plt.savefig('plot4_bid_volume.png')
plt.show()


#Plot5: Bid Price Plot
data3 = data.copy()
data2 = data.copy()
data3 = data3[data3['aFRR down EUR/MW_all'] < senario_price]
#remove zero values
data3 = data3[data3['aFRR down EUR/MW_all'] != 0]
data2 = data2[data2['aFRR down EUR/MW'] != 0]

fig, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(data3['timestamp'], data3['aFRR down EUR/MW_all'], 'o', label='Bud under prissetting', color='grey', alpha=0.5)
ax2.plot(data2['timestamp'], data2['aFRR down EUR/MW'], 'o', label='Bud over prissetting', color='blue')
ax2.axhline(y=senario_price, color='blue', linestyle='--', label='Prissettingsnivå')
ax2.set_ylim(0, 150)
ax2.set_ylabel('EUR/MW')
ax2.set_xlabel('Tid (time)')
ax2.set_title(f'Bud pris (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
ax2.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot5_bid_price.png')
plt.show()

#Plot6: Bud inntekt Plot
plt.figure(figsize=(10, 6))
plt.bar(data['timestamp'], data['revenue_reserve'], color='blue')
plt.xlabel('Tid (time)')
plt.ylabel('EUR')
plt.title(f'Bud inntekt (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.xticks(rotation=45)
plt.ylim(predefined_yaxis_EUR_low, predefined_yaxis_EUR_high)
plt.tight_layout()
plt.savefig('plot6_bid_income.png')
plt.show()

#Plot7: Aktiverings ladning Plot
plt.figure(figsize=(10, 6))
plt.bar(data['timestamp'], data['reserve_charge_MW'], color='blue')
plt.xlabel('Tid (time)')
plt.ylabel('MWh')
plt.title(f'Ladning ved aktivering (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.xticks(rotation=45)
plt.ylim(0, predefined_yaxis_MW_high)
plt.tight_layout()
plt.savefig('plot7_activation_charge.png')
plt.show()

#Plot8: Aktiverings pris Plot
plt.figure(figsize=(10, 6))
plt.bar(data['timestamp'], data['diff_mFRR_spot'], color='blue')
plt.xlabel('Tid (time)')
plt.ylabel('EUR/MWh')
plt.title(f'Differansen mellom ladet spotpris og kompensert mFRR ned pris (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.xticks(rotation=45)

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('plot8_activation_price.png')
plt.show()

#Plot9: Aktiverings inntekt Plot
plt.figure(figsize=(10, 6))
plt.bar(data['timestamp'], data['revenue_comp_reserve'], color='blue')
plt.xlabel('Tid (time)')
plt.ylabel('EUR')
plt.title(f'Kostnader ved aktiveringsladning (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.xticks(rotation=45)
plt.ylim(predefined_yaxis_EUR_low, predefined_yaxis_EUR_high)
plt.tight_layout()
plt.savefig('plot9_activation_income.png')
plt.show()


#Plot10: Total inntekt Plot
bar_data = data[['timestamp', 'revenue_reserve', 'revenue_comp_reserve', 'revenue_spot']]
bar_data = bar_data.set_index('timestamp')
# Prepare subplot layout
fig, ax = plt.subplots(figsize=(10, 6))
# Stacked bar chart for revenue components
ax.bar(bar_data.index, bar_data['revenue_spot'], label='Kostnader ved spotladning', color='red')
ax.bar(bar_data.index, bar_data['revenue_reserve'], label='Kompensasjon for kapasitet i aFRR ned  ', color='blue')
ax.bar(bar_data.index, bar_data['revenue_comp_reserve'], label='Kostnader ved aktiveringsladning', color='green')
ax.set_title(f'Total inntektstrøm per time. (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
ax.set_xlabel('Tid (time)')
ax.set_ylabel('EUR')
ax.set_ylim(predefined_yaxis_EUR_low, predefined_yaxis_EUR_high)
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot10_total_income.png')
plt.show()

#Plot12: Num_cars

plt.figure(figsize=(10, 6))
plt.plot(data['timestamp'], data['num_cars'], label='Antall parkerte biler')
plt.xlabel('Tid (time)')
plt.ylabel('Antall')
plt.title(f'Antall parkerte biler og ladestasjoner (scenario {senario_name}. Variabler; {senario_andel}%, {senario_price} EUR/MW)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot12_num_cars.png')
plt.show()


#reell spotladning og simulert spot og aktiveringsladning

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(data['timestamp'], data['spot_charge_MW'], color='green', label='Simulert ladning ved spot', alpha=0.5)
ax.bar(data['timestamp'], data['reserve_charge_MW'], bottom=data['spot_charge_MW'], color='blue', label='Simulert ladning ved aktivering', alpha=0.5)
ax.set_xlabel('Tid (time)')
ax.set_ylabel('MWh')
ax.set_title('Reell spotladning og simulert spot og aktiveringsladning')
ax.set_ylim(0, predefined_yaxis_MW_high)
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot11_simulert_spot_aktiveringsladning.png')
plt.show()

#reell spotladning
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(data['timestamp'], data['total_charged_energy'], color='grey', label='Reell spotladning', alpha=0.5)
# Formatting the plot
ax.set_xlabel('Tid (time)')
ax.set_ylabel('MWh')
#set y-axis to predefined values
ax.set_title('Reell spotladning')
ax.set_ylim(0, predefined_yaxis_MW_high)
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot12_reell_spotladning.png')
plt.show()

#reelle og simulerte kostnader

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(data['timestamp'], data['total_energy_cost'], color='grey', label='Reelle ladekostnader', alpha=0.5)
#ax.bar(data['timestamp'], data['rev_total'], color='blue', label='Simulerte ladekostnader', alpha=0.5)
# Formatting the plot
ax.set_xlabel('Tid (time)')
ax.set_ylabel('EUR')
ax.set_title('Reelle og simulerte ladekostnader')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plot12_reelle_simulerte_kostnader.png')
plt.show()


# Resample data to monthly
monthly_data = data.resample('ME', on='timestamp').agg({
    'rev_total': 'sum',
    'total_energy_cost': 'sum'
})
# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.35  # width of the bars
months = monthly_data.index.strftime('%Y-%m')
x = range(len(months))
ax.bar(x, monthly_data['rev_total'], width=width, label='Netto inntekt ved aFRR ned deltakelse', align='center')
ax.bar([p + width for p in x], monthly_data['total_energy_cost'], width=width, label='Reelle ladekostnader', align='center')
# Formatting the plot
ax.set_xlabel('Måned')
ax.set_ylabel('EUR')
ax.set_title('Månedlig netto inntekt ved aFRR ned deltakelse og reelle ladekostnader')
ax.set_xticks([p + width / 2 for p in x])
ax.set_xticklabels(months)
ax.legend()
plt.xticks(rotation=45)
#save figure
plt.savefig('plot13_månedlige_reelle_simulerte_kostnader.png')
plt.tight_layout()
plt.show()





############################################################################################################
#Nøkkelverdier
############################################################################################################

print('Reelle kostnader ved spotladning:', data['total_energy_cost'].sum(), 'EUR')

print('Simulerte kostnader ved spotladning:', data['revenue_spot'].sum(), 'EUR')
print('Simulert kompenasjon for kapasitet i aFRR ned:', data['revenue_reserve'].sum(), 'EUR')
print('Simulerte kostnader ved aktiveringsladning:', data['revenue_comp_reserve'].sum(), 'EUR')
print('Netto inntekt ved aFRR ned deltakelse:', data['rev_total'].sum(), 'EUR')

#print ny linje
print('\n')

#reelle spotladning MWh
print('Reell spotladning:', data['total_charged_energy'].sum(), 'MWh')
#simulert spotladning MWh
print('Simulert spotladning:', data['spot_charge_MW'].sum(), 'MWh')
#simulert aktiveringsladning MWh
print('Simulert aktiveringsladning:', data['reserve_charge_MW'].sum(), 'MWh')

#print ny linje
print('\n')

#simulert kapasitet i aFRR ned MW
print('Simulert kapasitet i aFRR ned:', data['bidding'].sum(), 'MW')
#ønsker å telle data['bidding'] som er større enn 0
print('Antall bud:', data[data['bidding'] > 0]['bidding'].count())