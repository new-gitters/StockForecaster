# prediction of stock price based on SVM
# Date: 2020-03-28
# Author: Jiahao Xia
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
import os

def GetData(filename):
    if filename.split('_')[1] == 'hist.csv':
        stockdata = pd.read_csv(filename, infer_datetime_format="%Y-%m-%d")
        stock_time = stockdata['time'].values
        stock_time = stock_time[::-1]
        stock_price = stockdata['open'].values
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
    else:
        stockdata = pd.read_csv(filename, infer_datetime_format="%Y-%m-%d %H:%M")
        stock_time = stockdata['time'].values
        stock_time = stock_time[::-1]
        stock_price = stockdata['price'].values
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
    return x, stock_price

def cv(x, stock_price, num_folds, cost, gamma):
    kf = KFold(n_splits=num_folds)
    absolute_error = np.array([])
    relative_error = np.array([])
    for train, validation in kf.split(x):
        x_train = x[train]
        x_validation = x[validation]
        stock_price_train = stock_price[train]
        stock_price_validation = stock_price[validation]
        model = SVR(kernel='rbf', C=cost, gamma=gamma)
        model.fit(x_train, stock_price_train)
        m_stock_price_validation = model.predict(x_validation)
        # accuracy evaluation
        average_absolute_error = np.nanmean(np.absolute(m_stock_price_validation - stock_price_validation))
        average_relative_error = np.nanmean(np.absolute(m_stock_price_validation - stock_price_validation) /
                                            stock_price_validation)
        absolute_error = np.append(absolute_error, average_absolute_error)
        relative_error = np.append(relative_error, average_relative_error)
    return np.nanmean(absolute_error), np.nanmean(relative_error)

def test(x_train, stock_price_train, x_test, stock_price_test, cost, gamma):
    model = SVR(kernel='rbf', C=cost, gamma=gamma)
    model.fit(x_train, stock_price_train)
    m_stock_price_test = model.predict(x_test)
    # accuracy evaluation
    absolute_error_test = np.nanmean(np.absolute(m_stock_price_test - stock_price_test))
    relative_error_test = np.nanmean(np.absolute(m_stock_price_test - stock_price_test) /
                                     stock_price_test)
    return absolute_error_test, relative_error_test

def main():
    if not os.path.exists('result_svm/'):
        os.makedirs('result_svm/')

    # read the stockdata
    file_folder = os.getcwd() + '\\stockdata\\*.csv'
    filenames = glob.glob(file_folder)
    # filenames = ['stockdata\\GOOG_hist.csv']
    accuracy_evaluation = pd.DataFrame(columns=['stock', 'absolute_error_validation', 'relative_error_validation',
                                                'absolute_error_test', 'relative_error_test'])
    parameters = pd.DataFrame(columns=['stock', 'cost', 'gamma'])
    # process each stock price data
    for filename in filenames:
        tmp = filename.split('\\')[-1]
        symbol = tmp.split('.')[0]
        # get data from file
        x, stock_price = GetData(filename)
        x_train0, x_test, stock_price_train0, stock_price_test = train_test_split(x, stock_price,
                                                                                  test_size=0.1)
        svr = GridSearchCV(SVR(kernel='rbf', gamma='scale'),
                           param_grid={"C": [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3],
                                       "gamma": np.logspace(-2, 2, 7)},
                           cv=5)
        svr.fit(x_train0.reshape(-1, 1), stock_price_train0)
        best_params = svr.get_params()
        best_cost = best_params['estimator__C']
        best_gamma = best_params['estimator__gamma']
        tmp_parameters = pd.DataFrame({'stock': [symbol],
                                       'cost': [best_cost],
                                       'gamma': [best_gamma]})
        parameters = parameters.append(tmp_parameters)
        # parameters.to_csv('result_svm/parameters.csv')

        # 5-fold cross validation
        absolute_error_validation, relative_error_validation = cv(x_train0.reshape(-1, 1),
                                                                  stock_price_train0, 5,
                                                                  best_cost, best_gamma)
        # test
        absolute_error_test, relative_error_test = test(x_train0.reshape(-1, 1), stock_price_train0,
                                                        x_test.reshape(-1, 1), stock_price_test,
                                                        best_cost, best_gamma)
        tmp_accuracy_evaluation = pd.DataFrame({'stock': [symbol],
                                                'absolute_error_validation': [absolute_error_validation],
                                                'relative_error_validation': [relative_error_validation],
                                                'absolute_error_test': [absolute_error_test],
                                                'relative_error_test': [relative_error_test]})
        accuracy_evaluation = accuracy_evaluation.append(tmp_accuracy_evaluation)
        # accuracy_evaluation.to_csv('result_svm/accuracy_evaluation.csv')

    parameters.to_csv('result_svm/parameters.csv')
    accuracy_evaluation.to_csv('result_svm/accuracy_evaluation.csv')

if __name__ == '__main__':
    main()

