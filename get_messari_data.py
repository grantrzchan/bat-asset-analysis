'''Script to download BTC, ETH and BAT data from Messari. Special thanks to Spenser Huang's article "Exploring Messari’s Crypto API", published 12/20/2018 on medium.com, for the insights
on how to leverage the API for the data. Check out Spenser's great article at https://medium.com/@spenserhuang/exploring-messaris-crypto-api-a7aa2c03fde2'''

from six.moves import urllib
import json
import csv
import numpy as np
import pandas as pd

tickers = ['BTC', 'ETH', 'BAT']
assets_list = []

#Let's limit the start and end date for the time series data to be between 2019-01-01 and 2021-03-01
ts_start = '2019-01-01'
ts_end = '2021-03-01'

for t in tickers:
    #for each ticker, get metrics from Messari API
    metrics_url = (f'https://data.messari.io/api/v1/assets/{t}/metrics')
    metrics_bytes = urllib.request.urlopen(metrics_url).read()
    metrics_json = metrics_bytes.decode('utf8')
    metrics_dict = json.loads(metrics_json)
    metrics_data = metrics_dict['data']
    #get profile
    profile_url = (f'https://data.messari.io/api/v1/assets/{t}/profile')
    profile_bytes = urllib.request.urlopen(profile_url).read()
    profile_json = profile_bytes.decode('utf8')
    profile_dict = json.loads(profile_json)
    profile_data = profile_dict['data']
    #get time series data
    ts_url= f'https://data.messari.io/api/v1/assets/{t}/metrics/price/time-series?start={ts_start}&end={ts_end}&interval=1d'
    ts_bytes = urllib.request.urlopen(ts_url).read()
    ts_json = ts_bytes.decode('utf8')
    ts_dict = json.loads(ts_json)
    ts_data = ts_dict['data']
    #for each ticker, combine data into a single output
    combined_data = dict()
    combined_data['ticker'] = t
    combined_data['metrics'] = metrics_data
    combined_data['profile'] = profile_data
    combined_data['time_series'] = ts_data
    assets_list.append(combined_data)

#writes output to a json file
json_output = json.dumps(assets_list)
f = open('assets_data.json', 'w')
f.write(json_output)
f.close()