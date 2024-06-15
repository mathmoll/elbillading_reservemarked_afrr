
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data
def load_data(file_path):
    return pd.read_excel(file_path)

# Function to preprocess data
def preprocess_data(data):
    data['date'] = data['timestamp'].dt.date
    data['hour'] = data['timestamp'].dt.hour
    return data

# Function to generate heatmaps for each relevant column
def generate_heatmaps(data, columns):
    for column in columns:
        if column == 'charge_MW' or not pd.api.types.is_numeric_dtype(data[column]):
            continue

        heatmap_data = data.pivot_table(values=column, index='date', columns='hour', aggfunc='mean')

        plt.figure(figsize=(15, 10))
        #sns.heatmap(heatmap_data, cmap="viridis", cbar_kws={'label': f'{column}'},vmax=800, vmin=0)
        sns.heatmap(heatmap_data, cmap="viridis", cbar_kws={'label': f'{column}'})
        plt.title(f'Hourly {column} Heatmap')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Date')
        plt.xticks(rotation=45)
        plt.tight_layout()
        #plt.savefig(f'{column}_heatmap.pdf')
        plt.show()

def main():
    file_path = '/Users/mathiasmollatt/Library/CloudStorage/OneDrive-NorwegianUniversityofLifeSciences/Materielle/01. Mathias/04. metode/M30-IØ nordic_syncron_area/df.xlsx'  # Update this path
    data = load_data(file_path)
    data = preprocess_data(data)

    relevant_columns = data.columns.difference(['timestamp', 'date', 'hour', 'Unnamed: 0'])
    generate_heatmaps(data, relevant_columns)


if __name__ == "__main__":
    main()
