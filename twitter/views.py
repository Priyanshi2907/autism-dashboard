from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import tweet
from .serializers import TweetSerializers
from .scraper import twitter_search  # Import your scraping function


class  SearchTweets(APIView):
    def get(self,request):
        related_keywords = [
          "Asperger's syndrome",
          "Autism spectrum disorder (asd)",
          "Asperger's syndrome",
          "Autism spectrum disorder (asd)",
          "Neurodevelopmental disorder",
          "Social communication",
          "Sensory processing",
          "Behavioral therapy",
          "Early intervention",
          "Special education",
          "Genetic factors",
          "Neurodiversity",
          "Social skills",
          "Cognitive deficits",
          "Speech therapy",
          "Pervasive developmental disorder (PDD)",
          "Executive function",
          "Applied behavior analysis (ABA)",
          "Communication difficulties",
          "Repetitive behaviors",
          "Hyperfocus",
          "Inclusion", 
          'Autism Spectrum Disorder', 
          'Pervasive Developmental Disorder',
          'Autism Support', 
          'Autistic Children', 
          'Special Needs', 
          'Developmental Disability', 
          'Learning Disability',
          'Sensory Processing Disorder',
          'Social Skills Training'
            ]
        for related_keyword in related_keywords:
            print("rlkey: ",related_keyword)
            # Scrape tweets using the keyword
            scraped_tweets,hashtag_count = twitter_search(related_keyword)
            print(type(scraped_tweets))
            if scraped_tweets is None:
                return Response("Failed to scrape tweets", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            # Save the scraped tweets to the database
            saved_tweets = []
            for i, tweet_data in scraped_tweets.iterrows():
    
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
                    tweet_id=tweet_data['tweet_id'],
                    text=tweet_data['text'],
                    created_at=tweet_data['created_at'],
                    tweet_link=tweet_data['tweet_link'],
                    user_screen_name=tweet_data['user_screen_name'],
                    user_location=tweet_data['user_location'],
                    user_followers_count = tweet_data['user_followers_count'],
                    user_friends_count = tweet_data['user_friends_count'],
                    retweet_count = tweet_data['retweet_count'],
                    favorite_count = tweet_data['favorite_count'],
                    lang=tweet_data['lang'],
                    reach = tweet_data['reach'],
                    hashtags=tweet_data['hashtags'],
    
                    
                )
                print("not here")
                tweet_obj.save()
                print("again here")
                saved_tweets.append(tweet_obj)
        
        # Serialize the saved tweets
        serializer = TweetSerializers(saved_tweets, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
