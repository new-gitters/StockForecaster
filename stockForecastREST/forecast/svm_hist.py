import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
import os
import pymysql
import sys
from sqlalchemy import create_engine
sys.path.insert(1, '../stockForecastREST')
from stockForecastREST.settings import DATABASES
DefaultSetting = DATABASES['default']

def GetData(symbol):
    conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
    cursor = conn.cursor()

    stockID=(symbol,)
    cursor.execute("SELECT * FROM ece568project.demo_historicaldata WHERE symbol=%s", stockID)
    stockdata=pd.DataFrame(data=cursor.fetchmany(size=20))
    #print(stockdata)
    stock_time = stockdata[2].values
    stock_time = stock_time[::-1]
    stock_price = stockdata[6].values
    stock_price = stock_price[::-1]
    stock_time_range = pd.date_range(pd.to_datetime(stock_time[0], format='%Y-%m-%d'),
                                         pd.to_datetime(stock_time[len(stock_time) - 1], format='%Y-%m-%d'),
                                         freq='D')

    stock_time_range = stock_time_range.values
    stock_time_range_index = np.arange(1, len(stock_time_range) + 1, 1)
    x = np.array([])
    stock_time = pd.to_datetime(stock_time, format='%Y-%m-%d')
    stock_time = stock_time.values
    for i in range(len(stock_time)):
        x = np.append(x, stock_time_range_index[stock_time_range == stock_time[i]])
    conn.close()
    return x, stock_price

def select_Period(symbol,start,end):
    conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
    cursor = conn.cursor()

    stockID=(symbol,)
    cursor.execute("SELECT * FROM ece568project.demo_historicaldata WHERE symbol=%s", stockID)
    stockdata=pd.DataFrame(data=cursor.fetchall())
    df = pd.DataFrame()
    #reverse the time from before to now
    stock_time = stockdata[2].values
    stock_time = stock_time[::-1]
    df['time']  =  pd.to_datetime(stock_time, format='%Y-%m-%d')
    stock_price = stockdata[6].values
    #reverse the stock price from before to now
    stock_price = stock_price[::-1]
    df['price'] = stock_price
    start= pd.to_datetime(start, format='%Y-%m-%d')
    end=pd.to_datetime(end, format='%Y-%m-%d')
   
    df=df.loc[(df['time'] > start) & (df['time'] < end)]
    period=df['time'].values
    prices=df['price'].values

    conn.close()
    return period,prices
    

def SVM_Prediction(symbol):
    x, stock_price = GetData(symbol)

    svr = GridSearchCV(SVR(kernel='rbf', gamma='scale'),
                           param_grid={"C": [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3],
                                       "gamma": np.logspace(-2, 2, 7)},
                           cv=5)
    svr.fit(x.reshape(-1, 1), stock_price)
     # predict
    best_params = svr.get_params()
    best_cost = best_params['estimator__C']
    best_gamma = best_params['estimator__gamma']
    model = SVR(kernel='rbf', C=best_cost, gamma=best_gamma)
    #print(x,stock_price)
    model.fit(x.reshape(-1, 1), stock_price)
    m_stock_price_test = model.predict(x[-1].reshape(-1, 1))
    tmp={}
    tmp['current']=stock_price[-1]
    tmp['forecast']=m_stock_price_test[0]
    return [tmp]


    
#print(select_Period('GOOG',"2020-03-05","2020-05-01"))

