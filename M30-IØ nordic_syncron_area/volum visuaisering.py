import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Last ned data
file_path = '/Users/mathiasmollatt/Library/CloudStorage/OneDrive-NorwegianUniversityofLifeSciences/Materielle/01. Mathias/04. metode/M30-IØ nordic_syncron_area/strategy.xlsx'
data = pd.read_excel(file_path)

# Konverter Datetime kolonne til datetime format
data['Datetime'] = pd.to_datetime(data['Datetime'])

# Sett Datetime kolonnen som index
data.set_index('Datetime', inplace=True)

# Resample data per uke som starter på mandag
weekly_mean = data.resample('W-Mon').mean()

# Tildel uketall
weekly_mean['Week_Number'] = weekly_mean.index.strftime('%U')

# Filtrer ut uker som ikke er fullstendige deler av året
#weekly_mean = weekly_mean[(weekly_mean['Week_Number'] != '00') & (weekly_mean['Week_Number'] != '53')]

# Plot de ukentlige gjennomsnittsverdiene for de valgte kolonnene med korrekte uketall
plt.figure(figsize=(12, 6))
plt.bar(weekly_mean.index, weekly_mean['aFRR down MW v2'], width=4, label='aFRR ned innkjøpt volum')
plt.bar(weekly_mean.index, weekly_mean['aFRR down MWh activated'], width=2, label='aFRR ned aktivert volum')

# Sett oppdaterte etiketter og tittel på norsk
plt.xlabel('Ukenummer')
plt.ylabel('Volum')
plt.title('Gjennomsnitlig innkjøpt og aktivert volum i aFRR ned i 2023')

#bytt ut x-aksen med uketall
plt.xticks(weekly_mean.index, weekly_mean['Week_Number'])



# Flytt legenden til øvre venstre hjørne
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
