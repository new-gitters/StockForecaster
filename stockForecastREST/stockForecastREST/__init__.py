"""
Database Init
"""
import pymysql
from stockForecastREST.db_init import *
from stockForecastREST.get_stock import getStockData
import threading


pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

stocks = ['GOOG', 'FB', 'MSFT', 'BABA', 'BILI','BIDU','TSLA', 'NVDA','AMZN','AAPL']
create_db()

def getStocks():
    data_hist = getStockData(stocks).get_historical_data()
    getStockData(stocks).store_historical_data(data_hist)
    data = getStockData(stocks).get_realtime_data()
    getStockData(stocks).store_realtime_data(data)
    print("Finish Downloading!")


thread1 = threading.Thread(target = getStocks)
thread1.start()