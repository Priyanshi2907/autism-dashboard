from django.core.management.base import BaseCommand
from datetime import datetime
from django.db.models import Count
from news.models import News
from twitter.models import tweet

class Command(BaseCommand):
    help = 'Calculate positive sentiment count for news and tweets by country'

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, help='Start date (YYYY-MM-DD)')
        parser.add_argument('end_date', type=str, help='End date (YYYY-MM-DD)')

    def handle(self, *args, **kwargs):
        start_date = datetime.strptime(kwargs['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(kwargs['end_date'], '%Y-%m-%d').date()

        # Fetch news and tweets data based on date range
        news_queryset = News.objects.filter(modified_dates__range=(start_date, end_date))
        tweet_queryset = tweet.objects.filter(created_at__range=(start_date, end_date))

        print("Taking Postive Count CountryWise....")
        # Calculate positive sentiment counts for news
        positive_news_counts = news_queryset.filter(sentiment='Positive').values('country').annotate(count=Count('country'))

        # Calculate positive sentiment counts for tweets
        positive_tweet_counts = tweet_queryset.filter(sentiment='Positive').values('country').annotate(count=Count('country'))

        combined_counts = {}
        for item in positive_news_counts:
            country = item['country']
            count = item['count']
            combined_counts[country] = combined_counts.get(country, 0) + count

        for item in positive_tweet_counts:
            country = item['country']
            count = item['count']
            combined_counts[country] = combined_counts.get(country, 0) + count

        # Display results
        self.stdout.write("Total Positive Sentiment Counts by Country for news and tweets:")
        for country, count in combined_counts.items():
            print(f"{country}: {count}")
        
        ##for negative Count
        print("Taking Negative Count CountryWise..........")
        # Calculate positive sentiment counts for news
        neg_news_counts = news_queryset.filter(sentiment='Negative').values('country').annotate(count=Count('country'))

        # Calculate positive sentiment counts for tweets
        neg_tweet_counts = tweet_queryset.filter(sentiment='Negative').values('country').annotate(count=Count('country'))

        combined_counts_neg = {}
        for item in neg_news_counts:
            country_neg = item['country']
            count_neg = item['count']
            combined_counts_neg[country_neg] = combined_counts_neg.get(country_neg, 0) + count_neg

        for item in neg_tweet_counts:
            country_neg = item['country']
            count_neg = item['count']
            combined_counts_neg[country_neg] = combined_counts_neg.get(country_neg, 0) + count_neg

        # Display results
        self.stdout.write("Total Negative Sentiment Counts by Country for news and tweets:")
        for country_neg, count_neg in combined_counts_neg.items():
            print(f"{country_neg}: {count_neg}")
