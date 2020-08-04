from alpha_vantage.timeseries import TimeSeries
import json
import os
from datetime import datetime

import pymysql
from stockForecastREST.settings import DATABASES
from stockForecastREST.settings import ALPHA_VANTAGE_KEY

from time import sleep

DefaultSetting = DATABASES['default']

class getStockData():
    def __init__(self, symbols):
        self.key = ALPHA_VANTAGE_KEY
        self.symbols = symbols
        self.ts = TimeSeries(self.key)

    def get_historical_data(self):
        data_list = []
        for symbol in self.symbols:
            data, meta_data = self.ts.get_daily(symbol)
            

            for time, info in data.items():
                format_str = '%Y-%m-%d'
                time = datetime.strptime(time, format_str).date()
                tmp = {'symbol': symbol,
                       'time': time,
                       'open': float(info['1. open']),
                       'high': float(info['2. high']),
                       'low': float(info['3. low']),
                       'close': float(info['4. close']),
                       'volume': int(info['5. volume'])}
                data_list.append(tmp)
            sleep(20)
        # print(data_list)
        # print(type(data_list))
        return data_list

    def get_realtime_data(self):
        data_list = []
        for symbol in self.symbols:
            data, meta_data = self.ts.get_intraday(symbol, interval='1min')
            

            for time, info in data.items():
                format_str = '%Y-%m-%d %H:%M:%S'
                time = datetime.strptime(time, format_str)
                tmp = {'symbol': symbol,
                       'time': time,
                       'price': float(info['4. close']),
                       'volume': int(info['5. volume'])}
                data_list.append(tmp)
            sleep(20)
        return data_list


    def store_historical_data(self, data_list):
        conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
        cursor = conn.cursor()
        for i, item in enumerate(data_list):
            cursor.execute("INSERT INTO demo_historicaldata (symbol, time, open, high, low, close, volume) "
                           "VALUES(%s, %s, %s, %s, %s, %s, %s)", (item['symbol'], item['time'],
                           item['open'], item['high'], item['low'], item['close'], item['volume']))
        conn.commit()
        conn.close()

    def store_realtime_data(self, data_list):
        conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
        cursor = conn.cursor()
        for i, item in enumerate(data_list):
            cursor.execute("INSERT INTO demo_realtimedata (symbol, time, price, volume) "
                           "VALUES(%s, %s, %s, %s)", (item['symbol'], item['time'], item['price'],
                                                                  item['volume']))
        conn.commit()
        conn.close()
