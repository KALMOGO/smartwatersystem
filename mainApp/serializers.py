from rest_framework import serializers
from .models import *

class WaterParametersIoT2Serializer(serializers.ModelSerializer):
    """
    """
    
    class Meta:
        model = waterParameters
        fields = ["ph","oxygen","turbidity","temperature", "site"]
        
    
class WaterParametersIoTSerializer(serializers.ModelSerializer):
    """
    """
    
    class Meta:
        model = waterParameters
        fields = ["ph","oxygen","turbidity","temperature","harvesting_time", "site"]
        
    
class WaterParametersPersonSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = waterParameters
        fields = ["id","ph","oxygen","turbidity","temperature","harvesting_time", "site"]

class WaterParameterPredSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = WaterParameterPred
        fields =("data_source", "parameter","upper_border", "lower_border")

class WaterQualityPredictionSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = WaterParameterPred
        fields = ("temperature")

class WaterQualityPredSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = WaterQualityPred
        fields = "__all__"
