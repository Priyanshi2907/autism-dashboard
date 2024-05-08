from rest_framework import serializers
from . models import *

class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model=News
        fields='__all__'

class RealTimeNewsSerializers(serializers.ModelSerializer):
    class Meta:
        model=News
        fields=['source','link','title','modified_dates']


        