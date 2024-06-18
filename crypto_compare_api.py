#makes an API call to cryptocompare to get data from a series of coins, and then upload it to a local postgresql database

import json
import requests
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2

#connection parameters
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = "5432"
database = "crypto_db"

def get_connection(): #from https://www.geeksforgeeks.org/connecting-to-sql-database-using-sqlalchemy-in-python/#
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )

engine = get_connection()

#input parameters
coins = ["BTC", "ETH", "SOL"]
days = "365"
features = ["time", "close"]

#main
for coin in coins:
    apiURL = ("https://min-api.cryptocompare.com/data/v2/histoday?fsym="+coin+"&tsym=USD&limit="+days+"&api_key=030b83dabcbc30883070a1dd3c189d92e51b8f2c2e6e0701970a0a9263c299d1")

    response = requests.get(apiURL)

    if response.status_code == 200:
        response = response.json()

        #get only the relevant header and put it in a df
        data = response["Data"]["Data"]
        result = pd.DataFrame(data)

        #get only the relevant columns, rename them to something easier to understand
        #result = result[features]
        #result.rename(columns={"time": "Time", "close": (coin+"_price")}, inplace=True)
        
        ''' #outputs as json for testing
        with open("out.txt", 'w') as output:
            outputText = result.to_string()
            output.write(outputText)
        '''
        result.to_sql(coin, engine, if_exists = 'replace', index = False)

        '''
        with open('api_data.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent = 4)
        '''

    else:
        print("Error retrieving API data")
