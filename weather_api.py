"""
##################################################
This script connect to Weatherbit API and downloads chosen data as JSON, 
based on provided CSV with ID (staring from 0), Lat, Lon (degrees) and year of observations.
##################################################
## Author: Tereza Novakova
## Copyright: Copyright 2022, weatherbitAPI
## Version: 1.0
## Mmaintainer: Tereza Novakova
## E-mail: teznovakova@gmail.com
"""

import json
import logging
import time
import urllib.request
from pprint import pprint

import pandas as pd


LOG_FILE = 'weatherapi_log.log'
LINK = 'https://api.weatherbit.io/v2.0/history/daily'
API_KEY = 'yourAPIkey'

#testing file with few selected rows
STATIONS_CSV = 'testovaci_csv.csv' 

#complete testing file
#STATIONS_CSV = 'argentina.csv'

#reading and opening file with stations, adding new columns for start and end date
STATIONS_DF = pd.read_csv(STATIONS_CSV)
STATIONS_DF['start_date'] = STATIONS_DF['Year'].astype(str) + '-01-01'
STATIONS_DF['end_date'] = (STATIONS_DF['Year'] + 1).astype(str) + '-01-01'


logging.basicConfig(filename=LOG_FILE, level = logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("spousteni:")

df_merge = []
#values for downloading
values = ['min_temp', 'max_temp', 'precip']

for num in range(len(STATIONS_DF)):
    time.sleep(0.5)

    #e.g. https://api.weatherbit.io/v2.0/history/daily?lat=-36.0502777777777&lon=-63.6080555555555&start_date=2021-01-01&end_date=2021-12-31&key=195f1d7f7130453c87c814ed0b3102b7
    link = LINK + f"?lat={STATIONS_DF.loc[num][1]}&lon={STATIONS_DF.loc[num][2]}&start_date={STATIONS_DF.loc[num][4]}&end_date={STATIONS_DF.loc[num][5]}&key={API_KEY}"
   
    pprint(link)

    #try to open URL with the link made above, if fails, stop
    try:
        req=urllib.request.Request(link, None, {'User-Agent': 'Opera/9.25 (Windows NT 5.1; U'})
        result = urllib.request.urlopen(req)
        logging.info('connected to: ' + link)
    except urllib.error.URLError as e:
        logging.critical('chyba: ' + e)
        break
    
    #load JSON from API
    json_data = json.load(result)
    #pprint(json_data)

    #create new json, convert python JSON object to variable
    with open(str(num + 1) + '_weatherbit_API.json', "w") as json_df:
        json.dump(json_data, json_df)

    #repeat as many times as there are values in the list of values, e.g. values = ['min_temp', 'max_temp', 'precip'] -> will repeat 3 times
    for value in values: 
        #pd.set_option('display.max_columns', None)
        #create dataframe from json, convert to row x column
        json_df = pd.json_normalize(json_data['data'])

        #transpose the data with datetime and chosen value
        # reset (erase) original index
        json_df = json_df[['datetime', value]].transpose().reset_index(drop = True)
        json_df.columns = json_df.iloc[0]
        json_df = json_df.iloc[1:].reset_index(drop = True)
        
        #insert new column with ID and set as index
        json_df.insert(0, 'ID', num + 1)
        json_df.set_index('ID')
        #pprint(json_df)
        
        #reset (erase) index and set new one on column ID
        STATIONS_DF.reset_index(drop = True).set_index('ID')

        #merge both dataframes using ID as index
        df_merge = pd.merge(STATIONS_DF, json_df, left_on = 'ID', right_on='ID')
        #pprint(df_merge)
        
        #delete columns that are not needed
        df_merge = df_merge.drop(columns = ['start_date', 'end_date'])
        if num == 0:
            #during the first repetition, create header for output csv
            df_merge.to_csv(f'{value}.csv', mode = 'a', header = True, index = False)
        else:
            #during the second... and so on repetition, do not create CSV header
            df_merge.to_csv(f'{value}.csv', mode = 'a', header = False, index = False)
