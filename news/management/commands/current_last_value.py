from django.core.management.base import BaseCommand
from news.models import News  # Import your model here
from datetime import datetime,timedelta
from django.db.models import Count
from twitter.models import tweet

class Command(BaseCommand):
    help = 'Fetch data from the database and display it in the terminal'

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        print("i m here")
        today = datetime.now()
        # Calculate the start and end dates of the previous month
        if today.month == 1:
            start_date = datetime(today.year - 1, 12, 1)
        else:
            start_date = datetime(today.year, today.month - 1, 1)
        end_date = datetime(today.year, today.month, 1) - timedelta(days=1)
        print("**",start_date)
        print("----",end_date)
        # Fetch data from the database based on the specified criteria
        news_data = News.objects.filter(modified_dates__gte=start_date, modified_dates__lte=end_date)
        print(news_data)
        # Calculate the total count of positive and negative sentiments
        news_sentiment_count = news_data.count()
        print("news count for previous : ",news_sentiment_count)

        tweet_data = tweet.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
        # Calculate the total count of all sentiments for tweets
        tweet_sentiments_count = tweet_data.count()
        print("tweet count for previuos : ",tweet_sentiments_count)
        total_previuos=news_sentiment_count+tweet_sentiments_count
        print("total count for previuos month : ",total_previuos)
        


        # for current month 
        print("for current month....")
        today = datetime.now()
        # Calculate the start and end dates of the current month
        start_date_c = datetime(today.year, today.month, 1)
        if today.month == 12:
            end_date_c = datetime(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date_c = datetime(today.year, today.month + 1, 1) - timedelta(days=1)

        news_data = News.objects.filter(modified_dates__gte=start_date_c, modified_dates__lte=end_date_c)
        # Calculate the total count of all sentiments for news
        news_sentiments_count_c = news_data.count()
        print("news count for current month : ",news_sentiments_count_c)
        
        # Fetch data from the "tweet" app based on the specified criteria
        tweet_data = tweet.objects.filter(created_at__gte=start_date_c, created_at__lte=end_date_c)
        # Calculate the total count of all sentiments for tweets
        tweet_sentiments_count_c = tweet_data.count()
        print("tweet count for current month : ",tweet_sentiments_count_c)
        total_current=tweet_sentiments_count_c+news_sentiments_count_c
        print("total count for current month : ",total_current)
        absolute_change=abs(total_previuos-total_current)
        print("absolute change :",abs(total_previuos-total_current))
        
        per_value=((absolute_change)/total_previuos)*100
        rounded_value=round(per_value,2)
        print("percentage_value : ",rounded_value)

        
        
        
        
        
        
        
        
        
        
        # Print the counts in the terminal
        # for sentiment_count in sentiments_count:
        #     print(f"Sentiment: {sentiment_count['sentiment']}, Count: {sentiment_count['count']}")
        #     #self.stdout.write(f"Sentiment: {sentiment_count['sentiment']}, Count: {sentiment_count['count']}")
