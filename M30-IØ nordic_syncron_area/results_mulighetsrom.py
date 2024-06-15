
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


import matplotlib.pyplot as plt
import pandas as pd

# Anta at data['timestamp'] er allerede konvertert til datetime, om ikke:
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Genererer en date_range som starter og slutter med datasettets min og max datoer
date_range = pd.date_range(start=data['timestamp'].min(), end=data['timestamp'].max(), freq='MS')

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(data['timestamp'], data['no_bid'], color='grey', alpha=0.3, label='Mulighetsrom fra elbiler ved ladning rett før avreise')
ax.axhline(y=1, color='lightseagreen', linestyle='--', label='Minste budgrense Statnett')
ax.axhline(y=0.436, color='orange', linestyle='--', label='Maksgrense for ladeanlegg')
ax.axhline(y=0.1, color='yellow', linestyle='--', label='Dagens effekttopp for ladeanlegg')

# Setter xticks til den første dagen i hver måned basert på den genererte date_range
ax.set_xticks(date_range)
ax.set_xticklabels([dt.strftime('%b') for dt in date_range])

plt.xlabel('Tid (måned)')
plt.ylabel('MW')
plt.title('Mulighetsrom for aFRR ned deltakelse for Gardermoen parkering i 2023')
plt.xticks(rotation=45)
plt.ylim(0, data['no_bid'].max() + 0.2)
plt.legend()
plt.tight_layout()
plt.savefig('Mulighetsrom for aFRR ned deltakelse for Gardermoen parkering i 2023.png')
plt.show()

