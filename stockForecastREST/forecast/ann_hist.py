

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import pandas as pd
import numpy as np
import os
import pymysql
import sys
from sqlalchemy import create_engine
#sys.path.insert(1, '../stockForecastREST')
from stockForecastREST.settings import DATABASES
DefaultSetting = DATABASES['default']

#for normalizing data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

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
    
def LSTM_Prediction(symbol):
#read the file
    conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
    cursor = conn.cursor()

    stockID=(symbol,)
    cursor.execute("SELECT * FROM ece568project.demo_historicaldata WHERE symbol=%s", stockID)
    df=pd.DataFrame(data=cursor.fetchall())

    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['time', 'close'])

    for i in range(0,len(data)):
        new_data['time'][i] = data[2][i]
        new_data['close'][i] = data[6][i]

#setting index
    new_data.index = new_data.time
    new_data.drop('time', axis=1, inplace=True)

#creating train and test sets
    dataset = new_data.values

    train = dataset[:,:]

#converting dataset into x_train and y_train
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(20,len(train)):
        x_train.append(scaled_data[i-20:i,0])
        y_train.append(scaled_data[i,0])
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

# create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=10, batch_size=1)

    inputs = new_data[:].values
    inputs = inputs.reshape(-1,1)
    inputs  = scaler.transform(inputs)

    X_test = []
    for i in range(20,inputs.shape[0]):
        X_test.append(inputs[i-20:i,0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)

    curr_price=scaler.inverse_transform(y_train[-1].reshape(-1, 1))[0][0]
    predict_price=closing_price[-1][0]
    tmp={}
    tmp['current']=curr_price
    tmp['forecast']=predict_price
    return [tmp]

#LSTM_Prediction('GOOG')

#print(select_Period('GOOG',"2020-03-05","2020-05-01"))

