# raw data taken from https://climate-change.canada.ca/climate-data/#/daily-climate-data
# download for top 10 population centers taken from 2021 Census of population

import pandas as pd
# Define a dictionary of weights for each station name
weights = {
    'BRANDON A': 0.5,
    'WINNIPEG CS A': 0.3
}
# List of file names to read in
#file_names = ['climate-daily.csv','climate-daily(1).csv', 'climate-daily(2).csv','climate-daily(2).csv','climate-daily(3).csv','climate-daily(4).csv','climate-daily(5).csv','climate-daily(6).csv','climate-daily(7).csv','climate-daily(8).csv','climate-daily(9).csv',]
file_names = ['test1.csv', 'test2.csv']

# Read in all CSV files and concatenate them into a single DataFrame
df = pd.concat([pd.read_csv(f) for f in file_names])

# Extract rows with a specific year (in this case, 2022)
year = 2022
data = df[df['LOCAL_YEAR'] == year]

# Write the filtered DataFrame to a new CSV file
#data.to_csv('{year}_filtered_data.csv', index=False)

# Convert 'DATE' column to datetime format
data['LOCAL_DATE'] = pd.to_datetime(data['LOCAL_DATE'])
# Add a new column for the weights based on the station name
data['WEIGHT'] = data['STATION_NAME'].map(weights)

# Calculate the weighted average temperature for each day based on the station name
daily_weighted_avg = data.groupby([data['LOCAL_DATE'].dt.date, 'STATION_NAME'])['MEAN_TEMPERATURE'].apply(
    lambda x: (x * data.loc[x.index, 'WEIGHT']).sum() / data.loc[x.index, 'WEIGHT'].sum()
)

# Unstack the data to create a pivot table with dates as rows and station names as columns
daily_weighted_avg = daily_weighted_avg.unstack()

# Save the daily average temperatures to a new CSV file for the current year
daily_weighted_avg.to_csv(f'weighted_average_temperatures.csv')