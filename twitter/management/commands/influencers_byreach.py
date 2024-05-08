from django.core.management.base import BaseCommand
from twitter.models import tweet
from twitter.serializers import ReachSerializer
import pandas as pd

class Command(BaseCommand):
    help = 'Get influencer list sorted by reach'

    def add_arguments(self, parser):
        parser.add_argument('entity', type=str, help='Entity (PERSON, ORG, All)')
        parser.add_argument('country', type=str, help='Country (optional)')
        parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
        parser.add_argument('end_date', type=str, help='End date (YYYY-MM-DD)')

    def handle(self, *args, **kwargs):
        entity = kwargs['entity']
        country = kwargs.get('country')
        start_date = kwargs['start_date']
        end_date = kwargs['end_date']

        # Filter tweets based on parameters
        if entity.lower() == 'all':
            queryset = tweet.objects.all()
        else:
            queryset = tweet.objects.filter(entity=entity)

        if country:
            queryset = queryset.filter(country=country)

        if start_date and end_date:
            queryset=queryset.filter(created_at__range=[start_date,end_date])
        

        # Sort influencer list by reach
        queryset = queryset.order_by('-reach')

        # Serialize influencer data
        serializer = ReachSerializer(queryset, many=True)
        df=pd.DataFrame(serializer.data)
        print(df)
        # Output serialized data
        #print(serializer.data)