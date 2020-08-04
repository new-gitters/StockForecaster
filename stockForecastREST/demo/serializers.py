from rest_framework import serializers 
from demo.models import HistoricalData
from demo.models import RealTimeData
 
 
class HistoricalDataSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = HistoricalData
        fields = ('symbol',
                  'time',
                  'open',
                  'high',
                  'low',
                  'close',
                  'volume')

class RealTimeDataSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = RealTimeData
        fields = ('symbol',
                  'time',
                  'price',
                  'volume')