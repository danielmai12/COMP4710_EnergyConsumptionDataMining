import os
import json
import csv
import datetime

# set the year to process data for
year = 2019
maxForAverages = 5

# set the input and output file paths
input_path = f'{year}_data'
output_path = f'{year}_averages'

# initialize a dictionary to store the daily averages
daily_averages = {}

# loop through each day's data
for filename in os.listdir(input_path):
    # parse the date from the filename
    date = datetime.datetime.strptime(filename, '%Y-%m-%d.json').date()
    # load the JSON data from the file
    with open(os.path.join(input_path, filename), 'r') as f:
        data = json.load(f)
#    print(data["return"][0])
    # loop through each asset and metered volume for the day
    for participant in range(len(data['return'])):
        for asset in data['return'][participant]['asset_list']:
            asset_id = asset['asset_ID']
            for metered_volume in asset['metered_volume_list']:
                # parse the metered volume as a float
                volume = float(metered_volume['metered_volume'])
                # add the volume to the daily total for the asset
                if asset_id not in daily_averages:
                    daily_averages[asset_id] = {}
                if date not in daily_averages[asset_id]:
                    daily_averages[asset_id][date] = {'total': 0, 'count': 0}
                daily_averages[asset_id][date]['total'] += volume
                daily_averages[asset_id][date]['count'] += 1

with open(output_path + '.json', 'w') as f:
    f.write(str(daily_averages))
    print(f'Saved data for {year} (json)')

# open the output file and write the headers
with open(output_path + '.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Day'] + list(daily_averages.keys()))

    # loop through each day and write the averages for each asset
    for i in range(365):
        date = datetime.date(year, 1, 1) + datetime.timedelta(days=i)
        row = [date.strftime('%Y-%m-%d')]
        for asset_id in daily_averages.keys():
            if date in daily_averages[asset_id]:
                average = daily_averages[asset_id][date]['total'] / daily_averages[asset_id][date]['count']
                row.append(average)
            else:
                row.append('')
        writer.writerow(row)

print(f'Saved data for {year} (csv)')



import requests
import datetime
import json

# set the API endpoint URL
url = 'https://api.aeso.ca/report/v1/assetlist?operating_status=ALL&asset_type=SINK'

# set the API key
headers = {
    'accept': 'application/json',
    'X-API-Key': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxOGpvM3oiLCJpYXQiOjE2NzcyNTcwNDV9.pVTJNIl8hNupvHLJ3cZmsJeAYWNd2dK1MC6fTcTXzOk'
}

responce = requests.get(url, headers=headers)
data = json.loads(responce.text)

assets = []
sink_daily_averages = {}


for asset in data['return']:
    assets.append(asset['asset_ID'])

for asset_id in daily_averages.keys():
    if asset_id in assets:
        sink_daily_averages[asset_id] = daily_averages[asset_id]    


# open the output file and write the headers
with open(output_path + '_sink.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Day'] + list(sink_daily_averages.keys()))

    # loop through each day and write the averages for each asset
    for i in range(365):
        date = datetime.date(year, 1, 1) + datetime.timedelta(days=i)
        row = [date.strftime('%Y-%m-%d')]
        for asset_id in sink_daily_averages.keys():
            if date in sink_daily_averages[asset_id]:
                average = sink_daily_averages[asset_id][date]['total'] / sink_daily_averages[asset_id][date]['count']
                row.append(average)
            else:
                row.append('')
        writer.writerow(row)

print(f'Saved data for {year} sinks (csv)')


averaged = {}

for i in range(365):
    date = datetime.date(year, 1, 1) + datetime.timedelta(days=i)
    averaged[date] = {'total': 0, 'count': 0}
    for asset_id in sink_daily_averages.keys():
        if date in sink_daily_averages[asset_id]:
            if sink_daily_averages[asset_id][date]['total'] > 0 and sink_daily_averages[asset_id][date]['total'] < maxForAverages:
#print(date, averaged[date]['total'], asset_id, sink_daily_averages[asset_id][date]['total'])
                averaged[date]['total'] +=  sink_daily_averages[asset_id][date]['total'] 
                averaged[date]['count'] += 1
                

with open(output_path + '_averaged.csv', 'w', newline='') as f:
    writer = csv.writer(f)
                    
    for i in range(365):
        date = datetime.date(year, 1, 1) + datetime.timedelta(days=i)
        row = [date.strftime('%Y-%m-%d')]
#print(averaged[date]['total'] ,averaged[date]['count'])
        averageVal = averaged[date]['total'] / averaged[date]['count']
        row.append(averageVal)

        writer.writerow(row)

    print(f'Saved data for {year} sinks averaged (csv)')