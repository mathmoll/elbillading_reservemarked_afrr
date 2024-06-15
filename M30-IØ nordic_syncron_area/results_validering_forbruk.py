import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

############################################
#Klargjør data
############################################


df = pd.read_excel('df.xlsx') #Open data and tidslinje
tidslinje = pd.read_excel('tidslinje.xlsx')
tidslinje.rename(columns={'Hour': 'timestamp'}, inplace=True) #change columna names from Hour to timestamp
df = df.merge(tidslinje, how='left', on='timestamp') #merge data and tidslinje
#data = data[['timestamp',  'num_cars', 'spot_charge_MW','spot_price', 'revenue_spot', 'total_charged_energy','spot', 'total_energy_cost']]
df = df[['timestamp',  'num_cars', 'spot_charge_MW', 'total_charged_energy']]
df.rename(columns={ 'spot_charge_MW': 'Ladning modell', 'total_charged_energy': 'Ladning reell'}, inplace=True) #Change names of columns
df['Ladning reell'] = df['Ladning reell']
df['Ladning modell'] = df['Ladning modell']*1000
df['charge_diff'] = df['Ladning reell'] - df['Ladning modell'] #calculate the difference between the total charged energy and the spot charge MW

#make excel file of data
df.to_excel('resultat_validering_forbruk.xlsx')

############################################
#Statistiske analyser
############################################

#calcuate MAPE
df['prosentvis_avvik'] = np.abs((df['charge_diff'] / df['Ladning reell'])) * 100
#change infinite values to NaN
df['prosentvis_avvik'] = df['prosentvis_avvik'].replace([np.inf, -np.inf], np.nan)
mape = np.mean(df['prosentvis_avvik'])

# Beregn Mean Absolute Error (MAE)
mae = np.mean(np.abs(df['Ladning reell'] - df['Ladning modell']))
# Beregn Root Mean Square Error (RMSE)
rmse = np.sqrt(np.mean((df['Ladning reell'] - df['Ladning modell']) ** 2))
# Beregn R-kvadrat
correlation_matrix = np.corrcoef(df['Ladning reell'], df['Ladning modell'])
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2




sum_ladning_reell = df['Ladning reell'].sum() #sum of the total charged energy
sum_ladning_modell = df['Ladning modell'].sum() #sum of the spot charge MW
sum_charge_diff = df['charge_diff'].sum() #sum of the difference between the total charged energy and the spot charge MW

print(sum_ladning_modell)
print(sum_ladning_reell)
print(sum_charge_diff)

############################################
#Plotting
############################################
sns.set(style="whitegrid") # Sett en stil for seaborn-plottene


# Korrelasjonsplot
plt.figure(figsize=(10, 6))
plt.scatter(df['Ladning reell'], df['Ladning modell'], alpha=0.5)
plt.title('Reelle verdier vs. Simulerte verdier')
plt.xlabel('Reelle Ladningsverdier [kWh/h]')
plt.ylabel('Simulerte Ladningsverdier [kWh/h]')
plt.plot([df['Ladning reell'].min(), df['Ladning reell'].max()], [df['Ladning reell'].min(), df['Ladning reell'].max()], 'k--', lw=2) # Identitetslinje
plt.tight_layout()
plt.savefig('korrelasjonsplot.png')
plt.show()

#Differanseplot
# Setter en mer estetisk tiltalende stil
sns.set(style="whitegrid")
# Opprett figur og akse
fig, ax = plt.subplots(figsize=(12, 6))
# Plot differansen som en linje
sns.lineplot(x=df['timestamp'], y=df['charge_diff'], ax=ax, color='blue', lw=1.5)
# Tilføy en horisontal linje ved y=0 for referanse
ax.axhline(0, color='red', linestyle='--')
# Tilpass plot
ax.set_title('Differansen mellom simulerte og reelle verdier', fontsize=16)
ax.set_xlabel('Tidspunkt', fontsize=12)
ax.set_ylabel('Differanse (kWh)', fontsize=12)
ax.figure.autofmt_xdate()  # Roter datoetiketter for bedre lesbarhet
#lagre figuren
plt.tight_layout()
#save figure
plt.savefig('differanseplot.png')
plt.show()



# Histogram for Ladning modell og Ladning reell
fig, axs = plt.subplots(1, 2, figsize=(14, 6)) # Sett opp figuren og akser
# Histogram for Ladning reell
sns.histplot(df['Ladning reell'], kde=False, ax=axs[1], bins=50)
axs[0].set_title('Histogram for reell ladning')
axs[0].set_xlabel('Reell ladning [kWh/h]')
axs[0].set_ylabel('Frekvens')
# Histogram for Ladning modell
sns.set(style="whitegrid")
sns.histplot(df['Ladning modell'], kde=False, ax=axs[0], bins=50)
axs[1].set_title('Histogram for simulert ladning')
axs[1].set_xlabel('Simulert ladning [kWh/h]')
axs[1].set_ylabel('Frekvens')
# Juster y-aksene for histogrammene for å matche hverandre
max_freq = max(axs[1].get_ylim()[1], axs[0].get_ylim()[1])
axs[1].set_ylim(0, max_freq)
axs[0].set_ylim(0, max_freq)
#juster x-aksene for histogrammene for å matche hverandre
max_freq = max(axs[1].get_xlim()[1], axs[0].get_xlim()[1])
axs[1].set_xlim(0, max_freq)
axs[0].set_xlim(0, max_freq)
#klargjør figuren
plt.tight_layout()
plt.savefig('histogram.png')
plt.show()

'''
#plot a line graph of the spot charge MW and the total charged energy
data.plot(x='timestamp', y=['Ladning modell', 'Ladning reell'], title='Ladning modell og reell ladning')
plt.show()

# Plotting av residuale verdier
plt.figure(figsize=(10, 6))
residuals = data['Ladning reell'] - data['Ladning modell']
plt.scatter(data.index, residuals, alpha=0.5)
plt.title('Residual Plot')
plt.xlabel('Observasjonsindeks')
plt.ylabel('Residualer')
plt.axhline(0, color='red', linestyle='--')
plt.show()
'''


#data.plot(x='timestamp', y=['spot_charge_MW', 'total_charged_energy'], title='Spot charge MW and total charged energy')
#plt.show()

#plot the difference between the total charged energy and the spot charge MW
#data.plot(x='timestamp', y='charge_diff', title='Difference between total charged energy and spot charge MW')
#plt.show()

#plot the percentage difference between the total charged energy and the spot charge MW
#data.plot(x='timestamp', y='prosentvis_avvik', title='Percentage difference between total charged energy and spot charge MW')
#plt.show()

#data['total_energy_cost'] = data['total_energy_cost'] * -1 #change total energy cost to negative values
#data['spot'] = data['spot'] * -1000 #change spot from kWh to MWh
#data['revenue_spot'] = data['revenue_spot'] * 11.6 #Change revenue spot to NOK
#data['rev_diff'] = data['total_energy_cost'] - data['revenue_spot'] #calculate the difference between the total energy cost and the revenue spot

#calculate the sum for total energy cost, revenue spot, total charged energy and spot charge MW

#sum_total_energy_cost = data['total_energy_cost'].sum()
#sum_revenue_spot = data['revenue_spot'].sum()


#plot the difference between the total energy cost and the revenue spot
#data.plot(x='timestamp', y='rev_diff', title='Difference between total energy cost and revenue spot')
#plt.show()

