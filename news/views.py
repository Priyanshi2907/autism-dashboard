from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import News
from twitter.models import tweet
from .serializers import NewsSerializers,RealTimeNewsSerializers
from django.utils import timezone

from .scraper import *
from django.db import transaction
from django.db.models import Count
from rest_framework.decorators import api_view

# Create your views here.

class PostNews(APIView):
    def get(self, request):
        print("post me hun")
        related_keywords = ["Autism spectrum disorder (asd)",
                            "Asperger's syndrome"
                            ]
        countries = ["Albania",
                     "Afghanistan"
                    ]   
        news_to_save = []     
        for related_keyword in related_keywords:
            for country in countries:
                keyword = related_keyword+' '+ country
                print("keyword from view : ",keyword)
                print(f'\n Fetching News articles for- {keyword} news\n')
       
                scraped_news = google_news_scraper(keyword) 
                #print (scraped_news)
                if scraped_news is None:
                    return Response("Failed to scrape news", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
                # Save the scraped tweets to the database in batches
               
                for index,news_data in scraped_news.iterrows():
                    print("news data : ",news_data)
                    news_obj = News(
                        country=news_data['country'],
                        source=news_data['source'],
                        link=news_data['link'],
                        title=news_data['title'],
                        date=news_data['date'],
                        description=news_data['description'],
                        modified_dates=news_data['Modified Dates'],
                        sentiment=news_data['sentiment']
                       
                    )
                    news_obj.save()
                    news_to_save.append(news_obj)
                    print("saved")
                # Batch insert tweets into the database
                # with transaction.atomic():
                #     News.objects.bulk_create(news_to_save)

        # Return response
        serializer = NewsSerializers(news_to_save, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def realtimenews(request, *args, **kwargs):
    sentiment = request.query_params.get('sentiment')
    country = request.query_params.get('country')
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')

    queryset = News.objects.all()

    if sentiment:
        queryset = queryset.filter(sentiment=sentiment)

    if country:
        queryset = queryset.filter(country=country)

    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        queryset = queryset.filter(modified_dates__gte=start_date)

    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        queryset = queryset.filter(modified_dates__lte=end_date)

    serializer = RealTimeNewsSerializers(queryset, many=True)
    return Response(serializer.data)


class SentimentStatistics(APIView):
    def get(self, request):
        # Get the dates for the previous month
        today =datetime.now()
        if today.month == 1:
            start_date_prev_month = datetime(today.year - 1, 12, 1)
        else:
            start_date_prev_month = datetime(today.year, today.month - 1, 1)
        end_date_prev_month = datetime(today.year, today.month, 1) - timedelta(days=1)

        # Calculate sentiment statistics for the previous month
        news_sentiment_count_prev_month = News.objects.filter(modified_dates__gte=start_date_prev_month, modified_dates__lte=end_date_prev_month).count()
        tweet_sentiment_count_prev_month = tweet.objects.filter(created_at__gte=start_date_prev_month, created_at__lte=end_date_prev_month).count()
        total_sentiment_count_prev_month = news_sentiment_count_prev_month + tweet_sentiment_count_prev_month

        # Get the dates for the current month
        start_date_current_month = datetime(today.year, today.month, 1)
        if today.month == 12:
            end_date_current_month = datetime(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date_current_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1)

        # Calculate sentiment statistics for the current month
        news_sentiment_count_current_month = News.objects.filter(modified_dates__gte=start_date_current_month, modified_dates__lte=end_date_current_month).count()
        tweet_sentiment_count_current_month = tweet.objects.filter(created_at__gte=start_date_current_month, created_at__lte=end_date_current_month).count()
        total_sentiment_count_current_month = news_sentiment_count_current_month + tweet_sentiment_count_current_month

        # Calculate absolute change
        absolute_change = abs(total_sentiment_count_prev_month - total_sentiment_count_current_month)

        # Calculate percentage change
        if total_sentiment_count_prev_month == 0:
            percentage_change = 0
        else:
            percentage_change = (absolute_change / total_sentiment_count_prev_month) * 100

        # Return the data as JSON response
        data = {
            "total_previous_month": total_sentiment_count_prev_month,
            "total_current_month": total_sentiment_count_current_month,
            "absolute_change": absolute_change,
            "percentage_change": round(percentage_change, 2)
        }
        return Response(data, status=status.HTTP_200_OK)
    
class CountryWiseCount(APIView):
    def get(self, request):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        country = request.query_params.get('country')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            news_queryset = News.objects.filter(modified_dates__range=(start_date, end_date))
            tweet_queryset = tweet.objects.filter(created_at__range=(start_date, end_date))
        else:
            news_queryset = News.objects.all()
            tweet_queryset = tweet.objects.all()

        if country:
            news_queryset = news_queryset.filter(country=country)
            tweet_queryset = tweet_queryset.filter(country=country)

        positive_news_counts = news_queryset.filter(sentiment='Positive').values('country').annotate(count=Count('country'))
        positive_tweet_counts = tweet_queryset.filter(sentiment='Positive').values('country').annotate(count=Count('country'))
        combined_positive_counts = self.combine_counts(positive_news_counts, positive_tweet_counts)

        negative_news_counts = news_queryset.filter(sentiment='Negative').values('country').annotate(count=Count('country'))
        negative_tweet_counts = tweet_queryset.filter(sentiment='Negative').values('country').annotate(count=Count('country'))
        combined_negative_counts = self.combine_counts(negative_news_counts, negative_tweet_counts)

        combined_counts = {}
        for country, count in combined_positive_counts.items():
            combined_counts[country] = {
                'positive_count': count,
                'negative_count': combined_negative_counts.get(country, 0),
                'total_count': count + combined_negative_counts.get(country, 0)
            }

        return Response(combined_counts, status=status.HTTP_200_OK)

    def combine_counts(self, queryset1, queryset2):
        combined_counts = {}
        for item in queryset1:
            country = item['country']
            count = item['count']
            combined_counts[country] = combined_counts.get(country, 0) + count

        for item in queryset2:
            country = item['country']
            count = item['count']
            combined_counts[country] = combined_counts.get(country, 0) + count

        return combined_counts
        
class LineChart(APIView):
    def get(self, request):
        country = request.query_params.get('country', None)
        sentiment = request.query_params.get('sentiment', None)
        start_date_str = request.query_params.get('start_date', None)
        end_date_str = request.query_params.get('end_date', None)

        # Calculate default start date (30 days ago)
        if not start_date_str:
            default_start_date = datetime.now().date() - timedelta(days=30)
            start_date_str = default_start_date.strftime('%Y-%m-%d')

        # Calculate end date if not provided (defaults to today)
        if not end_date_str:
            end_date_str = datetime.now().date().strftime('%Y-%m-%d')

        # Convert start and end date strings to date objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Filter news and tweets based on provided parameters
        news_queryset = News.objects.filter(modified_dates__range=(start_date, end_date))
        tweet_queryset = tweet.objects.filter(created_at__range=(start_date, end_date))

        if country:
            news_queryset = news_queryset.filter(country=country)
            tweet_queryset = tweet_queryset.filter(country=country)

        if sentiment:
            news_queryset = news_queryset.filter(sentiment=sentiment)
            tweet_queryset = tweet_queryset.filter(sentiment=sentiment)

        # Group news and tweets by date and count them
        news_counts_by_date = news_queryset.values('modified_dates').annotate(news_count=Count('id'))
        tweet_counts_by_date = tweet_queryset.values('created_at').annotate(tweet_count=Count('id'))

        # Merge news and tweet counts by date
        counts_by_date = {}
        for item in news_counts_by_date:
            date = item['modified_dates']
            counts_by_date[date] = {'news_count': item['news_count'], 'tweet_count': 0}
        for item in tweet_counts_by_date:
            date = item['created_at']
            if date in counts_by_date:
                counts_by_date[date]['tweet_count'] = item['tweet_count']
            else:
                counts_by_date[date] = {'news_count': 0, 'tweet_count': item['tweet_count']}

        # Calculate total count for each date
        for date, counts in counts_by_date.items():
            counts['total_count'] = counts['news_count'] + counts['tweet_count']

        # Construct the response
        response_data = []
        for date, counts in counts_by_date.items():
            data = {
                "date": date,
                "news_count": counts['news_count'],
                "tweet_count": counts['tweet_count'],
                "total_count": counts['total_count']
            }
            if country and sentiment:
                data["country"] = country
                data["sentiment"] = sentiment
            response_data.append(data)

        return Response(response_data, status=status.HTTP_200_OK)








# class SearchNews(APIView):
#     def get(self, request):
#         print("i m here")
#         start_date = request.query_params.get('start_date')
#         end_date = request.query_params.get('end_date')

#         if not start_date or not end_date:
#             return Response("start_date, and end_date are required.", status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Parse start_date and end_date strings to datetime objects
#             start_date = datetime.strptime(start_date, '%Y-%m-%d')
#             end_date = datetime.strptime(end_date, '%Y-%m-%d')
#         except ValueError:
#             return Response("Invalid date format. Date format should be 'YYYY-MM-DD'.", status=status.HTTP_400_BAD_REQUEST)

#         related_keywords = ["health","Autism spectrum disorder (asd)","Asperger's syndrome"]
#         countries = ["Albania"]
#                     #  ,"Afghanistan"]   
#         news_to_save = []     
#         for related_keyword in related_keywords:
#             for country in countries:
#                 keyword = related_keyword+' '+ country
#                 print("keyword from view : ",keyword)
#                 print(f'\n Fetching News articles for- {keyword} news\n')
       
#                 scraped_news = google_news_scraper(keyword,start_date,end_date) 
#                 #print (scraped_news)
#                 if scraped_news is None:
#                     return Response("Failed to scrape news", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#                 # Save the scraped tweets to the database in batches
               
#                 for index,news_data in scraped_news.iterrows():
#                     print("news data : ",news_data)
#                     news_obj = News(
#                         country=news_data['country'],
#                         source=news_data['source'],
#                         link=news_data['link'],
#                         title=news_data['title'],
#                         date=news_data['date'],
#                         description=news_data['description'],
#                         modified_dates=news_data['Modified Dates'],
#                         sentiment=news_data['sentiment']
                       
#                     )
#                     news_obj.save()
#                     news_to_save.append(news_obj)
        
#                 # Batch insert tweets into the database
#                 # with transaction.atomic():
#                 #     News.objects.bulk_create(news_to_save)

#         # Return response
#         serializer = NewsSerializers(news_to_save, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# def print_sentiments_counts_modified_yesterday():
#     # Get yesterday's date
#     yesterday = datetime.now() - timedelta(days=1)
#     print("yes date : ",yesterday)
#     # Query the database for records with modified dates equal to yesterday
#     news_objects = News.objects.filter(modified_dates=yesterday.date())
#     # Aggregate counts of positive and negative sentiments
#     sentiments_counts = news_objects.values('sentiment').annotate(count=Count('sentiment'))
#     print("sentiment : ",sentiments_counts)
#     # Print the counts in the terminal
#     for item in sentiments_counts:
#         print(f"Sentiment: {item['sentiment']}, Count: {item['count']}")

# #print_sentiments_counts_modified_yesterday()
