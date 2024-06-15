import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

###############################################
#Prepare data
###############################################

# Load your data here
data = pd.read_excel('summary_results.xlsx')
utvalgte_data = data.copy()

# Tegne liggende søylediagram
# Tegne liggende søylediagram
plt.figure(figsize=(18, 15))
max_rev = data['sum_rev'].max()  # Finn maksimal inntektsstrøm før loopen
for index, row in data.iterrows():
    if row['sum_rev'] == max_rev:
        color = 'green'
        label = 'Høyeste inntektsstrøm' if 'Høyeste inntektsstrøm' not in plt.gca().get_legend_handles_labels()[1] else None
    elif row['sum_failed_bids'] != 0:
        color = 'red'
        label = 'Mislykket deltakelse' if 'Mislykket deltakelse' not in plt.gca().get_legend_handles_labels()[1] else None
    else:
        color = 'blue'
        label = 'Inntektsstrøm' if 'Inntektsstrøm' not in plt.gca().get_legend_handles_labels()[1] else None
    plt.barh(index, row['sum_rev'], color=color, alpha=0.7, label=label)

# Sette opp tick labels
tick_labels = [f"{p}EUR/MW {s} andel" for p, s in zip(data['Prissetting'], data['Andel'])]
plt.yticks(range(len(data)), tick_labels)  # Sikre at etikettene samsvarer med dataindeksene
plt.grid(axis='y')
#inverter y-aksen
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.title('Inntektstrøm ved ulike variasjoner av prissetting og andel')
plt.xlabel('EUR')
plt.ylabel('Parameter kombinasjoner')

# Legge til legend
plt.legend()

plt.show()



#heatmap
# Anta at 'data' er et pandas DataFrame med relevante data
minste_bud_volum = 0.1
filtered_data = data[data['Minste bud volum'] == minste_bud_volum]
filtered_data['sum_rev'] = filtered_data['sum_rev'].where(filtered_data['sum_failed_bids'] == 0, 0)
# Modify the pivot table to flip the axes
pivot_table = filtered_data.pivot_table(index="Prissetting", columns="Andel", values="sum_rev")

# Continue with your setup, with the flipped axes pivot table
cmap = sns.light_palette((220, 100, 50), input="husl", as_cmap=True, reverse=True)
annotations = pivot_table.applymap(lambda x: 'Failed' if x == 0 else f'{x:.0f}').values

plt.figure(figsize=(14, 10))
mask = pivot_table == 0

enhanced_heatmap = sns.heatmap(pivot_table, annot=annotations, fmt="", cmap=cmap, linewidths=.5, linecolor='gray', mask=mask, cbar_kws={'label': 'Netto (EUR)'})
for text, value in zip(enhanced_heatmap.texts, pivot_table.to_numpy().flatten()):
    if pd.notna(value):
        text.set_color('black')

enhanced_heatmap.set_title(f'Inntektstrøm av prissetting og andel av maksimal bud (Minste bud volum = {minste_bud_volum} MW)', fontsize=16)
enhanced_heatmap.set_xlabel('Andel av maksimal bud', fontsize=14)
enhanced_heatmap.set_ylabel('Prissetting (EUR/MW)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('plot11_heatmap_flipped.png')
plt.show()


'''
#dataframen skal kun inneholde prissetting med verdi 50
utvalgte_data = utvalgte_data[utvalgte_data['Prissetting'] == 0]

#dataframen skal kun inneholde andel med verdi 0.7
utvalgte_data = utvalgte_data[utvalgte_data['Andel'] == 0.7]

df = pd.read_excel('data.xlsx')


###############################################
#Plotting fra data.xlsx (time for time)
###############################################

#make a stabled barplot of spot_charge_MW, reserve_charge_MW
# Prepare data for the stacked bar chart
bar_data = df[['timestamp', 'spot_charge_MW', 'reserve_charge_MW']]
bar_data = bar_data.set_index('timestamp')
# Prepare subplot layout
fig, ax = plt.subplots(figsize=(10, 10))
# Stacked bar chart for revenue components
ax.bar(bar_data.index, bar_data['spot_charge_MW'], label='Spot ladning (MW)', color='blue')
ax.bar(bar_data.index, bar_data['reserve_charge_MW'], bottom=bar_data['spot_charge_MW'], label='Aktiverings ladning (MW)', color='green')
ax.set_title('Spot- og aktiveringsladning per time')
ax.set_xlabel('Tid (Time)')
ax.set_ylabel('Ladning (MW)')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#make a stable barplot of sum_rev_spot, sum_rev_bids, sum_rev_comp
# Prepare data for the stacked bar chart
bar_data = df[['timestamp', 'revenue_reserve', 'revenue_comp_reserve', 'revenue_spot']]
bar_data = bar_data.set_index('timestamp')
# Prepare subplot layout
fig, ax = plt.subplots(figsize=(10, 10))
# Stacked bar chart for revenue components
ax.bar(bar_data.index, bar_data['revenue_reserve'], label='Inntekt fra bud', color='blue')
ax.bar(bar_data.index, bar_data['revenue_comp_reserve'], bottom=bar_data['revenue_reserve'], label='Inntekt fra kompensasjon', color='green')
ax.bar(bar_data.index, bar_data['revenue_spot'], bottom=bar_data['revenue_reserve']+bar_data['revenue_comp_reserve'], label='Kostnader fra spotladning', color='red')
ax.set_title('Total inntektstrøm per time')
ax.set_xlabel('Tid (time)')
ax.set_ylabel('Inntekt (NOK)')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#make a barplot of bidding
bar_data = df[['timestamp', 'bidding']]
bar_data = bar_data.set_index('timestamp')
fig, ax1 = plt.subplots(figsize=(10, 10))
ax1.bar(bar_data.index, bar_data['bidding'], label='Aksepterte bud', color='blue')
ax1.set_title('Aksepterte bud per time')
ax1.set_xlabel('Tid (time)')
ax1.set_ylabel('Budvolum (MW)')

ax2 = ax1.twinx()
#remove zero values from data['aFRR down EUR/MW']
df = df[df['aFRR down EUR/MW'] != 0]
#NOK to euro
df['aFRR down EUR/MW'] = df['aFRR down EUR/MW'] /11.6
ax2.plot(df['timestamp'], df['aFRR down EUR/MW'], 'o', label='Bud over prissetting' , color='red')
#put a line at 50
ax2.axhline(y=50, color='r', linestyle='--')
ax2.set_ylabel('Pris (EUR/MW)')
#set y-axis to start at 0
ax2.set_ylim(0, 150)

#remove zero values from plot
#change to dotplot
#ax2.plot(data['timestamp'], data['aFRR down EUR/MW'], 'o', color='red')
ax2.set_ylabel('Pris (EUR/MW)')

#join legend ax1 and ax2
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

'''





###############################################
#Plotting fra summary_results.xlsx (scenario)
###############################################
'''
#barplot fra inntekter
positions = range(len(utvalgte_data['Unnamed: 0']))

plt.bar([p - width * 1.5 for p in positions], utvalgte_data['sum_rev_spot'], width=width, color='salmon', label='Spot Kostnader (NOK)')
plt.bar([p - width * 0.5 for p in positions], utvalgte_data['sum_rev_bids'], width=width, color='skyblue', label='Bud inntekt (NOK)')
plt.bar([p + width * 0.5 for p in positions], utvalgte_data['sum_rev_comp'], width=width, color='lightgreen', label='Kompenasjon inntekt (NOK)')
plt.bar([p + width * 1.5 for p in positions], utvalgte_data['sum_rev'], width=width, color='gold', label='Total inntektstrøm (NOK)')

plt.xlabel('ID')
plt.ylabel('Inntekt/utgifter (NOK)')
plt.title('Detailed Revenue Comparison for Selected Entries')
plt.xticks([p for p in positions], utvalgte_data['Unnamed: 0'], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
'''





###############################################
#arkiv plot
###############################################


'''
# Unique values for 'Andel' and 'Minste bud volum'
unique_andels = data['Andel'].unique()
unique_min_buds = data['Minste bud volum'].unique()

# Prepare subplot layout for revenue
fig, axs = plt.subplots(len(unique_andels), len(unique_min_buds), figsize=(15, 10), sharex=True, sharey=False)

for i, andel in enumerate(sorted(unique_andels)):
    for j, min_bud in enumerate(sorted(unique_min_buds)):
        ax = axs[i, j]
        # Filter data for specific 'Andel' and 'Minste bud volum'
        filtered_data = data[(data['Andel'] == andel) & (data['Minste bud volum'] == min_bud)]

        # Stacked bar chart for revenues
        ax.bar(filtered_data['Prissetting'], filtered_data['sum_rev_spot'], label='Revenue from Spot Prices', color='blue')
        ax.bar(filtered_data['Prissetting'], filtered_data['sum_rev_bids'], bottom=filtered_data['sum_rev_spot'], label='Revenue from Bids', color='green')
        ax.bar(filtered_data['Prissetting'], filtered_data['sum_rev_comp'], bottom=filtered_data['sum_rev_spot'] + filtered_data['sum_rev_bids'], label='Revenue from Compensation', color='red')

        ax.set_title(f'Andel = {andel}, Minste bud volum = {min_bud}MW')
        ax.set_xlabel('Prissetting (EUR/MW)')
        ax.set_ylabel('Revenue (NOK)')

        if i == 0 and j == 0:  # Add legend only on the first plot for clarity
            ax.legend(loc='upper right')

# Adjust layout for revenue
plt.tight_layout()
plt.show()

# Prepare separate subplot layout for failed bids
fig, axs = plt.subplots(len(unique_andels), len(unique_min_buds), figsize=(15, 10), sharex=True, sharey=True)

for i, andel in enumerate(sorted(unique_andels)):
    for j, min_bud in enumerate(sorted(unique_min_buds)):
        ax = axs[i, j]
        # Filter data for specific 'Andel' and 'Minste bud volum'
        filtered_data = data[(data['Andel'] == andel) & (data['Minste bud volum'] == min_bud)]

        # Bar chart for failed bids
        ax.bar(filtered_data['Prissetting'], filtered_data['sum_failed_bids'], color='purple', label='Failed Bids')
        ax.set_title(f'Andel = {andel}, Minste bud volum = {min_bud}MW')
        ax.set_xlabel('Prissetting (EUR/MW)')
        ax.set_ylabel('Number of Failed Bids')

        if i == 0 and j == 0:  # Add legend only on the first plot for clarity
            ax.legend(loc='upper right')

# Adjust layout for failed bids
plt.tight_layout()
plt.show()





# Last inn dataene dine her
data_path = 'summary_results.xlsx'
data = pd.read_excel(data_path)

data1 = data.copy()

# Unike verdier for 'andel' og 'min_bud'
unique_andels = data['Andel'].unique()
unique_min_buds = data['Minste bud volum'].unique()

# Forbered subplot layout
fig, axs = plt.subplots(len(unique_andels), len(unique_min_buds), figsize=(15, 10), sharex=True, sharey=False)

for i, andel in enumerate(sorted(unique_andels)):
    for j, min_bud in enumerate(sorted(unique_min_buds)):
        ax = axs[i, j]
        # Filtrer data for spesifikk 'andel' og 'min_bud'
        filtered_data = data[(data['Andel'] == andel) & (data['Minste bud volum'] == min_bud)]

        # Stablet søylediagram for inntekter
        ax.bar(filtered_data['Prissetting'], filtered_data['sum_rev_spot'], label='Revenue from Spot Prices',
               color='blue')
        ax.bar(filtered_data['Prissetting'], filtered_data['sum_rev_bids'], bottom=filtered_data['sum_rev_spot'],
               label='Revenue from Bids', color='green')
        ax.bar(filtered_data['Prissetting'], filtered_data['sum_rev_comp'],
               bottom=filtered_data['sum_rev_spot'] + filtered_data['sum_rev_bids'], label='Revenue from Compensation',
               color='red')

        # Tilleggsakse for antall feilede bud
        ax_twin = ax.twinx()
        ax_twin.bar(filtered_data['Prissetting'], filtered_data['sum_failed_bids'], color='purple', width=0.4,
                    label='Failed Bids')
        ax_twin.set_ylabel('Number of Failed Bids')

        ax.set_title(f'Andel = {andel}, Minste bud volum = {min_bud}MW')
        ax.set_xlabel('Prissetting (EUR/MW)')
        ax.set_ylabel('Revenue (NOK)')

        if i == 0 and j == 0:  # Legg til legend kun på første plot for oversikt
            ax.legend(loc='upper left')
            ax_twin.legend(loc='upper right')

# Juster layout
plt.tight_layout()
plt.show()




# Last inn dataene dine
data = data1

# Filtrer ut de radene hvor det ikke er noen feilede bud
no_failed_bids = data[data['sum_failed_bids'] == 0]

# Sorter disse radene etter 'sum_rev' for å få de med høyest inntekt
top_scenarios = no_failed_bids.sort_values(by='sum_rev', ascending=False).head(3)

#make excel file of top_scenarios
#top_scenarios.to_excel('top_scenarios.xlsx')

# Sorter disse radene etter 'sum_rev' for å få de med høyest inntekt
#top_scenarios = no_failed_bids.sort_values(by='sum_rev', ascending=False)

# Vis dataene for å sikre at alt ser korrekt ut
print(top_scenarios)

#bruk denne koden med en for løkke for å plotte de tre beste scenariene
for i in top_scenarios.index:
    # Hent ut data for det spesifikke scenariet
    scenario = data.loc[i]

    # Legg inn data i specific_filter
    specific_filter = data[(data['Andel'] == scenario['Andel']) & (data['Minste bud volum'] == scenario['Minste bud volum'])]

    # Prepare data for the stacked bar chart
    bar_data = specific_filter[['Prissetting', 'sum_rev_spot', 'sum_rev_bids', 'sum_rev_comp']]

    # Prepare subplot layout
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Stacked bar chart for revenue components
    ax1.bar(bar_data['Prissetting'], bar_data['sum_rev_spot'], label='Revenue from Spot Prices', color='blue')
    ax1.bar(bar_data['Prissetting'], bar_data['sum_rev_bids'], bottom=bar_data['sum_rev_spot'], label='Revenue from Bids',
            color='green')
    ax1.bar(bar_data['Prissetting'], bar_data['sum_rev_comp'], bottom=bar_data['sum_rev_spot'] + bar_data['sum_rev_bids'],
            label='Revenue from Compensation', color='red')

    # Set title with specific 'andel' and 'min_bud'
    ax1.set_title(f'Revenue Breakdown by Prissetting (Andel = {scenario["Andel"]}, Minste bud volum = {scenario["Minste bud volum"]} MW)', fontsize=16)
    ax1.set_xlabel('Prissetting (EUR/MW)')
    ax1.set_ylabel('Revenue (NOK)')
    ax1.legend(loc='upper left')
    ax1.set_xticks(bar_data['Prissetting'])

    # Bar chart for number of failed bids
    ax2.bar(bar_data['Prissetting'], specific_filter['sum_failed_bids'], color='purple')
    ax2.set_title('Number of Failed Bids by Prissetting', fontsize=16)
    ax2.set_xlabel('Prissetting (EUR/MW)')
    ax2.set_ylabel('Number of Failed Bids')
    ax2.set_xticks(bar_data['Prissetting'])

    # Adjust layout
    plt.tight_layout()
    plt.show()





# Plotting av de tre beste scenariene
fig, ax = plt.subplots(figsize=(10, 6))

# Stablede søylediagrammer for de beste scenariene
ax.bar(top_scenarios['Prissetting'], top_scenarios['sum_rev_spot'], label='Revenue from Spot Prices', color='blue')
ax.bar(top_scenarios['Prissetting'], top_scenarios['sum_rev_bids'], bottom=top_scenarios['sum_rev_spot'], label='Revenue from Bids', color='green')
ax.bar(top_scenarios['Prissetting'], top_scenarios['sum_rev_comp'], bottom=top_scenarios['sum_rev_spot'] + top_scenarios['sum_rev_bids'], label='Revenue from Compensation', color='red')

ax.set_title('Top 3 Scenarios with Highest Revenue and No Failed Bids', fontsize=16)
ax.set_xlabel('Prissetting (EUR/MW)')
ax.set_ylabel('Revenue (NOK)')
ax.legend()

plt.show()

#plotting av de tre beste scenariene med antall feilede bud. Sett inn riktig Andel og Minste bud volum



# Filter data for specific 'andel' and 'min_bud'
specific_filter = data[(data['Andel'] == 0.7) & (data['Minste bud volum'] == 0.1)]

# Prepare data for the stacked bar chart
bar_data = specific_filter[['Prissetting', 'sum_rev_spot', 'sum_rev_bids', 'sum_rev_comp']]

# Prepare subplot layout
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Stacked bar chart for revenue components
ax1.bar(bar_data['Prissetting'], bar_data['sum_rev_spot'], label='Revenue from Spot Prices', color='blue')
ax1.bar(bar_data['Prissetting'], bar_data['sum_rev_bids'], bottom=bar_data['sum_rev_spot'], label='Revenue from Bids', color='green')
ax1.bar(bar_data['Prissetting'], bar_data['sum_rev_comp'], bottom=bar_data['sum_rev_spot'] + bar_data['sum_rev_bids'], label='Revenue from Compensation', color='red')


# Sett tittel med riktig 'andel' og 'min_bud'
ax1.set_title('Revenue Breakdown by Prissetting (Andel = 0.7, Minste bud volum = 0.1 MW)', fontsize=16)

ax1.set_xlabel('Prissetting (EUR/MW)')
ax1.set_ylabel('Revenue (NOK)')
ax1.legend(loc='upper right')
ax1.set_xticks(bar_data['Prissetting'])

# Bar chart for number of failed bids
ax2.bar(bar_data['Prissetting'], specific_filter['sum_failed_bids'], color='purple')
ax2.set_title('Number of Failed Bids by Prissetting', fontsize=16)
ax2.set_xlabel('Prissetting (EUR/MW)')
ax2.set_ylabel('Number of Failed Bids')
ax2.set_xticks(bar_data['Prissetting'])

# Adjust layout
plt.tight_layout()
plt.show()

'''

