from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import tweet
from .serializers import TweetSerializers
from .scraper import twitter_search  # Import your scraping function


class  SearchTweets(APIView):
    def get(self,request,keyword):
        # Scrape tweets using the keyword
        scraped_tweets,hashtag_count = twitter_search(keyword)
        print(type(scraped_tweets))
        if scraped_tweets is None:
            return Response("Failed to scrape tweets", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Save the scraped tweets to the database
        saved_tweets = []
        for i, tweet_data in enumerate(scraped_tweets):

            # Extract the count value from the pandas Series object
            #print("i",i)
            print("tweet data : ",tweet_data)
            # user_followers_count = scraped_tweets['user_followers_count'].iloc[i]
            # user_friends_count = scraped_tweets['user_friends_count'].iloc[i]
            # retweet_count = scraped_tweets['retweet_count'].iloc[i]
            # favorite_count = scraped_tweets['favorite_count'].iloc[i]
            # reach = scraped_tweets['reach'].iloc[i]
            # print("user_followers_count : ",user_followers_count)
            print(" i m here")
            tweet_obj = tweet(
                tweet_id=scraped_tweets['tweet_id'][i],
                text=scraped_tweets['text'][i],
                created_at=scraped_tweets['created_at'][i],
                tweet_link=scraped_tweets['tweet_link'][i],
                user_screen_name=scraped_tweets['user_screen_name'][i],
                user_location=scraped_tweets['user_location'][i],
                user_followers_count = scraped_tweets['user_followers_count'][i],
                user_friends_count = scraped_tweets['user_friends_count'][i],
                retweet_count = scraped_tweets['retweet_count'][i],
                favorite_count = scraped_tweets['favorite_count'][i],
                lang=scraped_tweets['lang'][i],
                reach = scraped_tweets['reach'][i],
                hashtags=scraped_tweets['hashtags'][i],

                
            )
            print("not here")
            tweet_obj.save()
            print("again here")
            saved_tweets.append(tweet_obj)
        
        # Serialize the saved tweets
        serializer = TweetSerializers(saved_tweets, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
