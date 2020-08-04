# StockFinalProject
Note: Before you can create the backend project, you need to install some requirements on your development machine. For Django, you need to have Python 3, PIP, and venv installed.

Bootstrap:

$cd stockforecast

$source ./bin/activate

$pip install django

$pip install djangorestframework

$pip install pymysql

$pip install django-cors-headers

and $pip install alpha-vantage

$pip install arrow

$pip install numpy

Setup MySQL Database Connection with 
Hostname: 127.0.0.1  port:3306
username: 'root' password: 'l1234567'    
Create a schema: 'ece568project'

Then hook up django with mysql database:

$cd stockForecastREST

$python manage.py migrate demo

Run up the server:

$python manage.py runserver --noreload 8080

Then use postman to test API:

1. post the historical data 
POST http://localhost:8080/api/demo/historicaldata
{
	 "symbol": "BLBL",
     "time": "2017-02-17",
     "open": 11.3,
     "high": 12.3,
     "low": 10.1,
     "close":11.3,
     "volume": 10


}

2.  get all the historical data
GET http://localhost:8080/api/demo/historicaldata

3. delete all the historical data
DELETE http://localhost:8080/api/demo/historicaldata

4. draw historical data
GET http://localhost:8080/api/drawdata/historical/GOOG/2020-03-05

5. draw real-time data
GET http://localhost:8080/api/drawdata/realtime/GOOG

6. get historical current price and prediction
GET http://localhost:8080/api/forecast/historical/GOOG/SVM

7. get realtime current price and prediction
GET http://localhost:8080/api/forecast/realtime/GOOG/SVM

8. get all companies' realtime current price 
GET http://localhost:8080/api/query/realtime

9. get highest stock price of any company in the last ten days
GET http://localhost:8080/api/query/highestinten/GOOG

10. get average stock price of any company in the latest one year
GET http://localhost:8080/api/query/avginoneyear/GOOG

11. get lowest stock price of any company in the latest one year
GET http://localhost:8080/api/query/lowestinoneyear/GOOG

12. List the ids of companies along with their name who have the average stock price lesser than the lowest of any of the Selected Company in the latest one year
GET http://localhost:8080/api/query/listoflow/GOOG

