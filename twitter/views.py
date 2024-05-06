from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import tweet
from .serializers import TweetSerializers
from datetime import datetime, timedelta

from .scraper import twitter_search  # Import your scraping function


class SearchTweets(APIView):
    def get(self, request):
        # Extract start_date and end_date from request query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # Convert start_date and end_date strings to datetime objects
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return Response("Invalid date format. Please use YYYY-MM-DD format.", status=status.HTTP_400_BAD_REQUEST)


       #list of keyword
        related_keywords = [
            "health",
            "autism",
            "Asperger's syndrome",
            "Autism spectrum disorder (asd)",
            "Neurodevelopmental disorder",
            "Social communication",
            # "Sensory processing",
            # "Behavioral therapy"
            # "Special education"
            # "Early intervention","Genetic factors","Neurodiversity",
            # "Social skills","Cognitive deficits","Speech therapy","Pervasive developmental disorder (PDD)"
            # ,"Executive function","Applied behavior analysis (ABA)","Communication difficulties","Repetitive behaviors","Hyperfocus",
            # "Inclusion", 'Autism Spectrum Disorder', 'Pervasive Developmental Disorder','Autism Support', 'Autistic Children', 
            # 'Special Needs', 'Developmental Disability', 'Learning Disability','Sensory Processing Disorder','Social Skills Training'
        ]
        countries = ["india","Afganistan"]
        saved_tweets = []
        for related_keyword in related_keywords:
            for country in countries:
                keyword=related_keyword+" "+country
                
        
                print("key: ", keyword)
                # Scrape tweets using the keyword
                scraped_tweets = twitter_search(keyword,start_date,end_date)
                print("in views : ",type(scraped_tweets))
                print(scraped_tweets)
                
                if scraped_tweets is None:
                    return Response("Failed to scrape tweets", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
                # Save the scraped tweets to the database
                for index, tweet_data in scraped_tweets.iterrows():
                    print("tweet data : ",tweet_data)
                    
                    tweet_obj = tweet(
                        tweet_id=tweet_data['tweet_id'],
                        text=tweet_data['text'],
                        created_at=tweet_data['created_at'],
                        tweet_link=tweet_data['tweet_link'],
                        user_screen_name=tweet_data['user_screen_name'],
                        user_location=tweet_data['user_location'],
                        user_followers_count=tweet_data['user_followers_count'],
                        user_friends_count=tweet_data['user_friends_count'],
                        retweet_count=tweet_data['retweet_count'],
                        favorite_count=tweet_data['favorite_count'],
                        lang=tweet_data['lang'],
                        reach=tweet_data['reach'],
                        hashtags=tweet_data['hashtags'],
                        country=tweet_data['country'],
                        sentiment=tweet_data['sentiment'],
                        entity=tweet_data['entity'],
                        name=tweet_data['username'],
                        user_profile_link=tweet_data['user_profile_link']
    
                    )
                    tweet_obj.save()
                    saved_tweets.append(tweet_obj)        
        # Serialize the saved tweets
        serializer = TweetSerializers(saved_tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    


    # user_followers_count = scraped_tweets['user_followers_count'].iloc[i]
                # user_friends_count = scraped_tweets['user_friends_count'].iloc[i]
                # retweet_count = scraped_tweets['retweet_count'].iloc[i]
                # favorite_count = scraped_tweets['favorite_count'].iloc[i]
                # reach = scraped_tweets['reach'].iloc[i]
                # print("user_followers_count : ",user_followers_count)
