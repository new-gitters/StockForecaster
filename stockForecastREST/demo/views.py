

"""
historicaldata_list(): GET list of historical data, POST a new entry of historical data, DELETE all historical data
realtimedata_list(): GET list of realtime data, POST a new entry of realtime data, DELETE all realtime data
"""
# Create your views here.
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from demo.models import HistoricalData
from demo.models import RealTimeData
from demo.serializers import HistoricalDataSerializer
from demo.serializers import RealTimeDataSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def historicaldata_list(request):
    #GET list of historical data, POST a new entry of historical data, DELETE all historical data
    if request.method == 'GET':
        historical_data = HistoricalData.objects.all()
        
        historical_serializer = HistoricalDataSerializer(historical_data, many=True)
        return JsonResponse(historical_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        historical_data = JSONParser().parse(request)
        historical_serializer = HistoricalDataSerializer(data=historical_data)
        if historical_serializer.is_valid():
            historical_serializer.save()
            return JsonResponse(historical_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(historical_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = HistoricalData.objects.all().delete()
        return JsonResponse({'message': '{} Historical Data were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'POST', 'DELETE'])
def realtimedata_list(request):
    #GET list of realtime data, POST a new entry of realtime data, DELETE all realtime data
    if request.method == 'GET':
        realtime_data = RealTimeData.objects.all()
        
        realtime_serializer = RealTimeDataSerializer(realtime_data, many=True)
        return JsonResponse(realtime_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        realtime_data = JSONParser().parse(request)
        realtime_serializer = RealTimeDataSerializer(data=realtime_data)
        if realtime_serializer.is_valid():
            realtime_serializer.save()
            return JsonResponse(realtime_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(realtime_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = RealTimeData.objects.all().delete()
        return JsonResponse({'message': '{} RealTime Data were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)