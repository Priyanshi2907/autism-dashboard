from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from news.models import News
from twitter.models import tweet


class Command(BaseCommand):
    help = 'Calculate total count of news and tweets by country and sentiment'

    def add_arguments(self, parser):
        parser.add_argument('country', type=str, help='Country')
        parser.add_argument('sentiment', type=str, help='Sentiment (positive/negative)')
        parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
        parser.add_argument('end_date', type=str, help='End date (YYYY-MM-DD)')

    def handle(self, *args, **kwargs):
        country = kwargs['country']
        sentiment = kwargs['sentiment']
        start_date = datetime.strptime(kwargs['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(kwargs['end_date'], '%Y-%m-%d').date()

        # Fetch news and tweets data based on parameters
        news_queryset = News.objects.filter(country=country, modified_dates__range=(start_date, end_date))
        tweet_queryset = tweet.objects.filter(country=country, created_at__range=(start_date, end_date))

        # Calculate count of news and tweets based on sentiment
        if sentiment == 'Positive':
            news_count = news_queryset.filter(sentiment='Positive').count()
            tweet_count = tweet_queryset.filter(sentiment='Positive').count()
        elif sentiment == 'Negative':
            news_count = news_queryset.filter(sentiment='Negative').count()
            tweet_count = tweet_queryset.filter(sentiment='Negative').count()
        else:
            raise ValueError("Sentiment must be either 'positive' or 'negative'")

        # Display results
        print(f"Total Count of {sentiment.capitalize()} News and Tweets for {country} from {start_date} to {end_date}:")
        print(f"News Count: {news_count}")
        print(f"Tweet Count: {tweet_count}")
