from django.http.response import JsonResponse


from rest_framework.decorators import api_view
from forecast.bayesian_hist import Bayesian_Prediction as Bayesian_Prediction_Hist
from forecast.bayesian_real import Bayesian_Prediction as Bayesian_Prediction_Real
from forecast.svm_hist import SVM_Prediction as SVM_Prediction_Hist
from forecast.svm_real import SVM_Prediction as SVM_Prediction_Real
from forecast.ann_hist import LSTM_Prediction as LSTM_Prediction_Hist
from forecast.ann_real import LSTM_Prediction as LSTM_Prediction_Real


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def historical(request,symbol,choice):
    #GET list of historical data, POST a new entry of historical data, DELETE all historical data
    if request.method == 'GET':
        if choice=='bayesian':
            data=Bayesian_Prediction_Hist(symbol)
        elif choice=='svm':
            data=SVM_Prediction_Hist(symbol)
        else:
            data=LSTM_Prediction_Hist(symbol)
        return JsonResponse(data, safe=False)
        # 'safe=False' for objects serialization
        
@api_view(['GET', 'POST', 'DELETE'])
def realtime(request,symbol,choice):
    #GET list of historical data, POST a new entry of historical data, DELETE all historical data
    if request.method == 'GET':
        if choice=='bayesian':
            data=Bayesian_Prediction_Real(symbol)
        elif choice=='svm':
            data=SVM_Prediction_Real(symbol)
        else:
            data=LSTM_Prediction_Real(symbol)
        return JsonResponse(data, safe=False)
        # 'safe=False' for objects serialization