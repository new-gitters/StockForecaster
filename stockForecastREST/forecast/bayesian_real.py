import pymysql
import sys
sys.path.insert(1, '../stockForecastREST')
from stockForecastREST.settings import DATABASES
import pandas as pd
DefaultSetting = DATABASES['default']

import numpy as np
import arrow

alpha = 5e-3
beta = 11.1
degree = 7


def read_in_database(symbol):
    conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
    cursor = conn.cursor()

    stockID=(symbol,)
    cursor.execute("SELECT * FROM ece568project.demo_realtimedata WHERE symbol=%s", stockID)
    stockdata=pd.DataFrame(data=cursor.fetchmany(size=20))
    #print(stockdata)
    stock_time = stockdata[2].values
    stock_time = stock_time[::-1]
    stock_price = stockdata[3].values
    stock_price = stock_price[::-1]
    stock_time_range = pd.date_range(pd.to_datetime(stock_time[0], format='%Y-%m-%d %H:%M'),
                                         pd.to_datetime(stock_time[len(stock_time) - 1], format='%Y-%m-%d %H:%M'),
                                         freq='min')
    stock_time_range = stock_time_range.values
    stock_time_range_index = np.arange(1, len(stock_time_range) + 1, 1)
    x = np.array([])
    stock_time = pd.to_datetime(stock_time, format='%Y-%m-%d %H:%M')
    stock_time = stock_time.values
    for i in range(len(stock_time)):
        x = np.append(x, stock_time_range_index[stock_time_range == stock_time[i]])
    x_raw = x[:]
    y_raw = stock_price[:]
    x_today = [x[-1]]
    y_today = [stock_price[-1]]
    
    return np.asarray(x_raw), np.asarray(y_raw), np.asarray(x_today), np.asarray(y_today)
def phi(x):
    phi = [[x**i] for i in range(degree + 1)]
    return np.asarray(phi)


# formula (1.70), mean
def mx(x,S,x_train, y_train):
    return beta*(phi(x).T).dot(S).dot(np.sum([t*phi(xt) for xt, t in zip(x_train, y_train)], axis=0))[0][0]


# formula (1.71), variance
def s2x(x,S):
    return (1/beta + (phi(x).T).dot(S.dot(phi(x))))[0][0]

        


def Bayesian_Prediction(symbol):
   
    x_all, y_all, x_t, y_t = read_in_database(symbol)
    #print(x_all)
    #print(y_all)
    #print(x_t)
    #print(y_t)
    '''
    # x_train = x_all[int(len(x_all)/3):]
    # y_train = y_all[int(len(y_all)/3):]
    # x_test = x_all[:int(len(x_all)/3)]
    # y_test = y_all[:int(len(y_all)/3)]
    '''
    # x_train = x_all[::-1]
    # y_train = y_all[::-1]
    N = len(x_all)
    x_train = np.arange(0, 1.0, 1.0 / N)
    x_test = np.arange(0, 1.0 + 1.0 / N, 1.0 / N)

    # formula (1.72)
  
    S_inv = alpha * np.identity(degree + 1) + beta * np.sum([phi(x).dot(phi(x).T) for x in x_train], axis=0)
    S = np.linalg.inv(S_inv)

    #plt.plot(x_test, [mx(x) for x in x_test], color='0')
    #for x, t in zip(x_train, y_train):
        #plt.scatter(x, t, color='b')
    #print(x_train)
    #print(x_test)
    predict_v = mx(x_test[-2],S,x_train, y_all)
    variance = s2x(x_test[-2],S)
    #print("The prediction of N+1 time is", predict_v, "+-", variance)
    #print("The real value is", y_t)

    tmp={}
    tmp['forecast']=predict_v
    tmp['current']=y_t
    return [tmp]

#print(Bayesian_Prediction('GOOG'))