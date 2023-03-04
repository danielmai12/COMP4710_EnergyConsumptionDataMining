#curl -X 'GET' \
#  'https://api.aeso.ca/report/v1/meteredvolume/details?startDate=2018-01-01&endDate=2019-01-01' \
#  -H 'accept: application/json' \
#  -H 'X-API-Key: eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxOGpvM3oiLCJpYXQiOjE2NzcyNTcwNDV9.pVTJNIl8hNupvHLJ3cZmsJeAYWNd2dK1MC6fTcTXzOk'

import requests
import datetime

# set the API endpoint URL
url = 'https://api.aeso.ca/report/v1/meteredvolume/details'

# set the API key
headers = {
    'accept': 'application/json',
    'X-API-Key': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxOGpvM3oiLCJpYXQiOjE2NzcyNTcwNDV9.pVTJNIl8hNupvHLJ3cZmsJeAYWNd2dK1MC6fTcTXzOk'
}

# set the year to download data for
year = 2019
folder = str(year) + "_data"

# set the start and end dates for the loop
start_date = datetime.date(year, 1, 1)
#end_date = datetime.date(year, 1, 2)
end_date = datetime.date(year, 12, 31)

# loop through each day and download the data
for i in range((end_date - start_date).days + 1):
    date = start_date + datetime.timedelta(days=i)
    params = {
        'startDate': date.strftime('%Y-%m-%d')
    }
    response = requests.get(url, headers=headers, params=params)
    filename = f'{folder}/{date.strftime("%Y-%m-%d")}.json'
    with open(filename, 'w') as f:
        f.write(response.text)
    print(f'Saved data for {date} to {filename}')
