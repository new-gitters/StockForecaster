from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from drawdata.function import select_Hist
from drawdata.function import select_Realtime
# Create your views here.
# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def historical(request,symbol,start):
    #GET list of historical data, POST a new entry of historical data, DELETE all historical data
    if request.method == 'GET':
        data=select_Hist(symbol,start)
        return JsonResponse(data, safe=False)
def realtime(request,symbol):
    #GET list of historical data, POST a new entry of historical data, DELETE all historical data
    if request.method == 'GET':
        data=select_Realtime(symbol)
        return JsonResponse(data, safe=False)
