import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from sklearn.metrics import r2_score
from statsmodels.tsa.seasonal import seasonal_decompose


#open data and tidslinje
df = pd.read_excel('data.xlsx')
tidslinje = pd.read_excel('tidslinje.xlsx')

#change columna names from Hour to timestamp
tidslinje.rename(columns={'Hour': 'timestamp'}, inplace=True)

#merge data and tidslinje
df = df.merge(tidslinje, how='left', on='timestamp')

#keep only the columns we want
#data = data[['timestamp',  'num_cars', 'spot_charge_MW','spot_price', 'revenue_spot', 'total_charged_energy','spot', 'total_energy_cost']]
df = df[['timestamp',  'num_cars', 'revenue_spot', 'total_energy_cost']]

#Change names of columns
df.rename(columns={ 'total_energy_cost': 'Inntektstrøm modell', 'revenue_spot': 'Inntektstrøm reell'}, inplace=True)


df['Inntektstrøm reell'] = df['Inntektstrøm reell'] * 11.6
df['Inntektstrøm modell'] = df['Inntektstrøm modell']
df['Inntektstrøm_diff'] = df['Inntektstrøm modell'] - df['Inntektstrøm reell'] #calculate the difference between the total charged energy and the spot charge MW


# Beregn Mean Absolute Error (MAE)
mae = np.mean(np.abs(df['Inntektstrøm reell'] - df['Inntektstrøm modell']))

# Beregn Root Mean Square Error (RMSE)
rmse = np.sqrt(np.mean((df['Inntektstrøm reell'] - df['Inntektstrøm modell']) ** 2))

# Beregn R-kvadrat
correlation_matrix = np.corrcoef(df['Inntektstrøm reell'], df['Inntektstrøm modell'])
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2

# Sett opp plottestil
sns.set(style="whitegrid")

# Plotting av faktiske verdier mot predikerte verdier
plt.figure(figsize=(10, 6))
plt.scatter(df['Inntektstrøm reell'], df['Inntektstrøm modell'], alpha=0.5)
plt.title('Faktiske verdier vs. Predikerte verdier')
plt.xlabel('Faktiske Inntektstrømsverdier')
plt.ylabel('Predikerte Inntektstrømsverdier')
plt.plot([df['Inntektstrøm reell'].min(), df['Inntektstrøm reell'].max()], [df['Inntektstrøm reell'].min(), df['Inntektstrøm reell'].max()], 'k--', lw=2) # Identitetslinje
plt.show()

# Plotting av residuale verdier
plt.figure(figsize=(10, 6))
residuals = df['Inntektstrøm reell'] - df['Inntektstrøm modell']
plt.scatter(df.index, residuals, alpha=0.5)
plt.title('Residual Plot')
plt.xlabel('Observasjonsindeks')
plt.ylabel('Residualer')
plt.axhline(0, color='red', linestyle='--')
plt.show()


sum_ladning_reell = df['Inntektstrøm reell'].sum() #sum of the total charged energy
sum_ladning_modell = df['Inntektstrøm modell'].sum() #sum of the spot charge MW
sum_charge_diff = df['Inntektstrøm_diff'].sum() #sum of the difference between the total charged energy and the spot charge MW

print(sum_ladning_modell)
print(sum_ladning_reell)
print(sum_charge_diff)

#make excel file of data
df.to_excel('resultat_validering_Inntektstrøm.xlsx')

#plot a line graph of the spot charge MW and the total charged energy
df.plot(x='timestamp', y=['Inntektstrøm modell', 'Inntektstrøm reell'], title='Inntektstrøm modell og reell')
plt.show()

#plot the difference between the total charged energy and the spot charge MW
df.plot(x='timestamp', y='Inntektstrøm_diff', title='Forskjell mellom Inntektstrøm modell og reell')
plt.show()




data = df

# Visning av de første fem radene
data.head()

# Deskriptiv statistikk
descriptive_stats = data.describe()

# T-test for middelverdier
t_stat, p_value = ttest_ind(data['Inntektstrøm reell'], data['Inntektstrøm modell'])

# Korrelasjonsanalyse
correlation = data['Inntektstrøm reell'].corr(data['Inntektstrøm modell'])

# Feilanalyse
mae = np.mean(np.abs(data['Inntektstrøm reell'] - data['Inntektstrøm modell']))
rmse = np.sqrt(np.mean((data['Inntektstrøm reell'] - data['Inntektstrøm modell'])**2))

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(data['timestamp'], data['Inntektstrøm reell'], label='Reell Inntektstrøm', alpha=0.7)
plt.plot(data['timestamp'], data['Inntektstrøm modell'], label='Modell Inntektstrøm', alpha=0.7)
plt.title('Reell vs Modell Inntektstrøm')
plt.xlabel('Tid')
plt.ylabel('Inntektstrøm')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# R^2 beregning
r2 = r2_score(data['Inntektstrøm reell'], data['Inntektstrøm modell'])

# Flere plot
fig, axes = plt.subplots(2, 1, figsize=(14, 12))
axes[0].plot(data['timestamp'], data['Inntektstrøm reell'], label='Reell Inntektstrøm', alpha=0.7)
axes[0].plot(data['timestamp'], data['Inntektstrøm modell'], label='Modell Inntektstrøm', alpha=0.7)
axes[0].set_title('Reell vs Modell Inntektstrøm')
axes[0].set_xlabel('Tid')
axes[0].set_ylabel('Inntektstrøm')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(data['timestamp'], data['Inntektstrøm_diff'], label='Forskjell (Reell - Modell)', color='red', alpha=0.7)
axes[1].set_title('Forskjell mellom Reell og Modellert Inntektstrøm')
axes[1].set_xlabel('Tid')
axes[1].set_ylabel('Inntektsforskjell')
axes[1].legend()
axes[1].grid(True)
plt.tight_layout()
plt.show()

# Beregning av residualer
data['Residuals'] = data['Inntektstrøm reell'] - data['Inntektstrøm modell']

# Histogram av residualer
plt.figure(figsize=(10, 6))
sns.histplot(data['Residuals'], kde=True, color='blue')
plt.title('Histogram av Residualer')
plt.xlabel('Residualverdier')
plt.ylabel('Frekvens')
plt.grid(True)
plt.show()

# Sesongmessig dekomponering, antar daglig data
decompose_result = seasonal_decompose(data.set_index('timestamp')['Inntektstrøm reell'], model='additive', period=24)
fig = decompose_result.plot()
fig.set_size_inches(14, 10)
fig.tight_layout()
plt.show()

# Box-plot analyse
plt.figure(figsize=(10, 6))
sns.boxplot(data=data['Inntektstrøm reell'])
plt.title('Box-Plot av Reelle Inntektstrømmer')
plt.xlabel('Inntektstrøm')
plt.grid(True)
plt.show()
