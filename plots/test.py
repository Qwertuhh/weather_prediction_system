import pandas as pd


ladc_data = pd.read_csv('data/raw/HADC/location_1.csv')
print(ladc_data.head())  # Display the first few rows of the DataFrame
temperature = float(loc_row['temp'])
print(temperature)