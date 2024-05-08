from rest_framework import serializers
from . models import tweet

class TweetSerializers(serializers.ModelSerializer):
    class Meta:
        model=tweet
        fields='__all__'

class ReachSerializer(serializers.ModelSerializer):
    class Meta:
        model=tweet
        fields = ['name', 'reach','user_profile_link']

class RealTimeTweetSerializer(serializers.ModelSerializer):
    class Meta:
        model=tweet
        fields = ['tweet_id', 'text','created_at','tweet_link','user_screen_name']
