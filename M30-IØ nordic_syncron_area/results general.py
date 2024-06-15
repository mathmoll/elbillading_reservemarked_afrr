import matplotlib.pyplot as plt

# Updated scenario names with line breaks for readability
updated_scenarios = [
    "Faktiske kostnader\n(ukontrollert ladning)",
    "Simulerte kostnader\n(ladning ved ankomst)",
    "Simulerte kostnader\n(ladning ved avreise)",
    "aFRR ned deltakelse\n(scenario budgrense)",
    "aFRR ned deltakelse\n(scenario anleggsgrense)",
    "aFRR ned deltakelse\n(scenario effektgrense)",
]

net_cash_flows = [-9141,-9122, -8767, -5047, 1691, -3]  # Net cash flows for each scenario

# Create the bar plot
plt.figure(figsize=(9, 5))
bars = plt.barh(updated_scenarios[::-1], net_cash_flows[::-1], color='lightseagreen')
plt.xlabel('Netto kontantstrøm (EUR)')
plt.title('Kontantstrøm for ladning av elbiler med og uten markedsdeltakelse for 2023')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Center-align the values within the bars
for bar, value in zip(bars, net_cash_flows[::-1]):
    x_position = bar.get_width() / 2 if value > 0 else bar.get_width() / 2
    plt.text(x_position, bar.get_y() + bar.get_height()/2, f'{value} EUR', va='center', ha='center', color='black')

# Save the plot to a file
plt.tight_layout()
plt.savefig('resultat general.png')
plt.show()
