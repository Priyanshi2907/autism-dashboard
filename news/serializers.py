from rest_framework import serializers
from . models import *

class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model=News
        fields='__all__'