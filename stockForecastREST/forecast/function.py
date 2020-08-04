import pymysql
from stockForecastREST.settings import DATABASES

DefaultSetting = DATABASES['default']

import numpy as np
import arrow

alpha = 5e-3
beta = 11.1
degree = 7

def read_in_database(rows):
    x_raw = []
    y_raw = []
    x_today = []
    y_today = []
    

    # get timestamp and the price of close today
    x_today.append(arrow.get(rows[0][2]).replace(tzinfo='US/Pacific').timestamp)
    y_today.append(float(rows[0][6]))
    for row in rows[1:]:
            # get timestamp and the price of close every day before
        timestamp = arrow.get(row[2]).replace(tzinfo='US/Pacific').timestamp
        x_raw.append(timestamp)
        y_raw.append(float(row[6]))
    # get the earliest timestamp
    time_earliest = arrow.get(rows[-1][2]).replace(tzinfo='US/Pacific').timestamp
    # calculate the number of days from the earliest day
    x_raw = [int((i-time_earliest)/86400) for i in x_raw]
    x_today = [int((x_today[0]-time_earliest)/86400)]
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
    conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
    cursor = conn.cursor()

    stockID=(symbol,)
    cursor.execute("SELECT * FROM ece568project.demo_historicaldata WHERE symbol=%s", stockID)

#rows=cursor.fetchmany(size=20)
#read_in_csv(rows)
    data=cursor.fetchmany(size=20)
    #print(data)
    rows=[]
    for row in data:
        tmp=list(row)
        tmp[2]=tmp[2].strftime("%Y/%m/%d")
        rows.append(tmp)
    
    x_all, y_all, x_t, y_t = read_in_database(rows)
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
    y_train = y_all[::-1]
    x_test = np.arange(0, 1.0 + 1.0 / N, 1.0 / N)

    # formula (1.72)
  
    S_inv = alpha * np.identity(degree + 1) + beta * np.sum([phi(x).dot(phi(x).T) for x in x_train], axis=0)
    S = np.linalg.inv(S_inv)

    #plt.plot(x_test, [mx(x) for x in x_test], color='0')
    #for x, t in zip(x_train, y_train):
        #plt.scatter(x, t, color='b')
    #print(x_train)
    #print(x_test)
    predict_v = mx(x_test[-2],S,x_train, y_train)
    variance = s2x(x_test[-2],S)
    #print("The prediction of N+1 time is", predict_v, "+-", variance)
    #print("The real value is", y_t)

    res=[]
    for row in rows:
        tmp={}
        tmp['price']=float(row[6])
        tmp['date']=row[2]
        res.append(tmp)
    tmp={}
    tmp['price']=predict_v
    tmp['date']=str(rows[0][2])
    res.append(tmp)
    return res

#Bayesian_Prediction('GOOG')





