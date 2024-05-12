from rest_framework import serializers
from . models import *

class RSerializers(serializers.ModelSerializer):
    class Meta:
        model=rwords
        fields='__all__'
    
class TSerializers(serializers.ModelSerializer):
    class Meta:
        model=tt
        fields='__all__'

class HSerializers(serializers.ModelSerializer):
    class Meta:
        model=hashtags
        fields='__all__'