import pymysql
import sys
import numpy as np
sys.path.insert(1, '../stockForecastREST')
from stockForecastREST.settings import DATABASES
import pandas as pd
DefaultSetting = DATABASES['default']


def select_Realtime(symbol):
    conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
    cursor = conn.cursor()

    stockID=(symbol,)
    cursor.execute("SELECT * FROM ece568project.demo_realtimedata WHERE symbol=%s", stockID)
    stockdata=pd.DataFrame(data=cursor.fetchmany(size=12))
    #reverse the time from before to now
    stock_time = stockdata[2].values
    stock_time = stock_time[::-1]
    df = pd.DataFrame()
    df['time']  =  pd.to_datetime(stock_time, format='%Y-%m-%d %H:%M')
    stock_price = stockdata[3].values
    #reverse the stock price from before to now
    stock_price = stock_price[::-1]
    df['price'] = stock_price
    res=[]
    for i in range(len(stock_time)):
        tmp={}
        tmp['time']="{}:{}".format(df['time'].values[i].dt.hour,df['time'].values[i].dt.minute)
        tmp['price']=stock_price[i]
        res.append(tmp)
    conn.close()
    return res



    
def select_Hist(symbol,start):
    conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
    cursor = conn.cursor()

    stockID=(symbol,)
    cursor.execute("SELECT * FROM ece568project.demo_historicaldata WHERE symbol=%s", stockID)
    stockdata=pd.DataFrame(data=cursor.fetchall())
    
    df = pd.DataFrame()
    stock_time = stockdata[2].values
    stock_time = stock_time[::-1]
    df['time']  =  pd.to_datetime(stock_time, format='%Y-%m-%d')
    stock_price = stockdata[6].values
    stock_price = stock_price[::-1]
    table={}
    #print(type(stock_time[0]))
    for i in range(len(stock_price)):
        t=stock_time[i].strftime("%Y-%m-%d")
        table[t]=stock_price[i]

    #select the date after the start date
    df=df.loc[df['time'] > start]

    points=[5,6,7,8,9,10,11,12]

    if len(df['time'])<=30:
        point=5
    else:
        point=points[(len(df['time'])-30)//10]
    
    stock_price = stockdata[6].values
    stock_price = stock_price[::-1]
    stock_time_range = pd.date_range(pd.to_datetime(start, format='%Y-%m-%d'),
                                         pd.to_datetime(stock_time[len(stock_time) - 1], format='%Y-%m-%d'),
                                         freq='D')

    stock_time_range = stock_time_range.values
   
    #print('stock time range',stock_time_range)
    stock_time_range_index = np.arange(0, len(stock_time_range), 1)
    #print('range index',stock_time_range_index)
    #print(len(stock_time_range_index))
    x = np.array([])
    stock_time = pd.to_datetime(stock_time, format='%Y-%m-%d')
    stock_time = stock_time.values
    for i in range(len(stock_time)):
        x = np.append(x, stock_time_range_index[stock_time_range == stock_time[i]])
    
    idx=np.round(np.linspace(0,len(x)-1,point)).astype(int)
    selected_idx=np.array(x[idx]).astype(int)
    selected=stock_time_range[selected_idx]
    #print(selected)
    res=[]
    for item in selected:
        tmp={}
        item = pd.to_datetime(item, format='%Y-%m-%d')
        t=item.strftime("%Y-%m-%d")
        tmp['time']=t
        tmp['price']=table[t]
        res.append(tmp)
    conn.close()
    return res
    



#res=select_Hist('FB','2019-12-18')
#print(res)