from django.core.management.base import BaseCommand
from twitter.models import tweet
from twitter.serializers import RealTimeTweetSerializer
import pandas as pd

class Command(BaseCommand):
    help = 'Get influencer list sorted by reach'

    def add_arguments(self, parser):
        parser.add_argument('sentiment', type=str, help='sentiment (Positive, Negative)')
        parser.add_argument('country', type=str, help='Country (optional)')
        parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
        parser.add_argument('end_date', type=str, help='End date (YYYY-MM-DD)')

    def handle(self, *args, **kwargs):
        sentiment = kwargs['sentiment']
        country = kwargs.get('country')
        start_date = kwargs['start_date']
        end_date = kwargs['end_date']
        
        

        if sentiment:
            queryset=tweet.objects.filter(sentiment=sentiment)
        if country:
            queryset=queryset.filter(country=country)
        if start_date and end_date:
            queryset=queryset.filter(created_at__range=[start_date,end_date])
        
        

        serializers=RealTimeTweetSerializer(queryset,many=True)

        df=pd.DataFrame(serializers.data)
        print(df)
        
