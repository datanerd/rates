# use twelvedata to get historical share price for a given stock symbol
# use https://api.twelvedata.com/time_series?symbol=${symbol}&interval=1day&start_date=${startDate}&apikey=${apiKey} API call format
# access API key and stock symbol as command line arguments

import requests
import json
import sys
import os
import datetime
from datetime import datetime

start_date = '2000-01-01'


# Get the API key from command line arguments
api_key = sys.argv[1]

# Get the stock symbol from command line arguments
stock_symbol = sys.argv[2]

# make the API call to twelvedata to get the historical share price
# save date and close price to a file
# make file name in the format ${stock_symbol}.json
url = f'https://api.twelvedata.com/time_series?symbol={stock_symbol}&interval=1day&start_date={start_date}&apikey={api_key}'
response = requests.get(url)
json_response = response.json()
file_name = f'{stock_symbol}.json'
with open(file_name, 'w') as file:
    json.dump(json_response, file)

