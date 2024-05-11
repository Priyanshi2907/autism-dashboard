from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import tweet
from .serializers import TweetSerializers,ReachSerializer,RealTimeTweetSerializer
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
import itertools
# from .date_scraper import twitter_search  # Import your scraping function
from . scraper_tweet import *
import ast
from langdetect import detect,LangDetectException

class PostTweets(APIView):
    def get(self, request):
        print("View post of tweets")
        #list of keyword
        related_keywords = [
            #"education",
            # "health",
            "autism",
            "Asperger's syndrome",
            "Autism spectrum disorder (asd)",
            "Neurodevelopmental disorder",
            "Social communication",
            "Sensory processing",
            "Behavioral therapy"
            "Special education"
            "Early intervention","Genetic factors","Neurodiversity",
            "Social skills","Cognitive deficits","Speech therapy","Pervasive developmental disorder (PDD)"
            ,"Executive function","Applied behavior analysis (ABA)","Communication difficulties","Repetitive behaviors","Hyperfocus",
            "Inclusion", 'Autism Spectrum Disorder', 'Pervasive Developmental Disorder','Autism Support', 'Autistic Children', 
            'Special Needs', 'Developmental Disability', 'Learning Disability','Sensory Processing Disorder','Social Skills Training'
        ]
        # countries = ["india","Afganistan"]
        saved_tweets = []
        for related_keyword in related_keywords:
            # for country in countries:
                keyword=related_keyword        
                print("key: ", keyword)
                # Scrape tweets using the keyword
                scraped_tweets = twitter_search(keyword)
                print("in views : ",type(scraped_tweets))
                print(scraped_tweets)
                
                if scraped_tweets is None:
                    return Response("Failed to scrape tweets", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
                # Save the scraped tweets to the database
                for index, tweet_data in scraped_tweets.iterrows():
                    print("tweet data : ",tweet_data)
                    if not tweet.objects.filter(tweet_id=tweet_data['tweet_id']).exists():

                        tweet_obj = tweet(
                            tweet_id=tweet_data['tweet_id'],
                            text=tweet_data['text'],
                            created_at=tweet_data['created_at'],
                            tweet_link=tweet_data['tweet_link'],
                            user_screen_name=tweet_data['user_screen_name'],
                            #user_location=tweet_data['user_location'],
                            user_followers_count=tweet_data['user_followers_count'],
                            #user_friends_count=tweet_data['user_friends_count'],
                            #retweet_count=tweet_data['retweet_count'],
                            #favorite_count=tweet_data['favorite_count'],
                            #lang=tweet_data['lang'],
                            # reach=tweet_data['reach'],
                            # hashtags=tweet_data['hashtags'],
                            country=tweet_data['country'],
                            # sentiment=tweet_data['sentiment'],
                            # entity=tweet_data['entity'],
                            profile_pic=tweet_data['profile_pic'],
                            name=tweet_data['username'],
                            user_profile_link=tweet_data['user_profile_link']
        
                        )
                        tweet_obj.save()
                        saved_tweets.append(tweet_obj)  
                        print("tweets saved")  
                    else:
                        print("Tweet with ID {} already exists, skipping...".format(tweet_data['tweet_id']))
    
        # Serialize the saved tweets
        serializer = TweetSerializers(saved_tweets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    


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
        countries = ["india","Afghanistan","Albania"]
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

class getdata(APIView):
    def get(self,request):

        queryset=tweet.objects.all()
        serializer = TweetSerializers(queryset, many=True)
        return Response(serializer.data)
    
class NameByReach(APIView): 
    def get(self, request, *args, **kwargs):
        entity = self.request.query_params.get('entity')
        country = self.request.query_params.get('country')
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        queryset = tweet.objects.all()

        if entity:
            queryset = queryset.filter(entity=entity)

        if country:
            queryset = queryset.filter(country=country)

        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__gte=start_date)

        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__lte=end_date)

        queryset = queryset.order_by('-reach')

        serializer = ReachSerializer(queryset, many=True)
        return Response(serializer.data)
    
class RealTimeTweet(APIView):
    def get(self, request, *args, **kwargs):
        sentiment = self.request.query_params.get('sentiment')
        country = self.request.query_params.get('country')
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        queryset = tweet.objects.all()

        if sentiment:
            queryset = queryset.filter(sentiment=sentiment)

        if country:
            queryset = queryset.filter(country=country)

        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__gte=start_date)

        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__lte=end_date)

        serializer = RealTimeTweetSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def hashtag_pairs(request):
    country = request.query_params.get('country', None)
    start_date = request.query_params.get('start_date', None)
    end_date = request.query_params.get('end_date', None)

    # Parse start and end dates if provided
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Filter tweets based on parameters
    queryset = tweet.objects.all()

    if country:
        queryset = queryset.filter(country=country)

    if start_date and end_date:
        queryset = queryset.filter(created_at__range=[start_date, end_date])
   
    # Function to check if a string contains only English characters
    def is_english(text):
        return bool(re.match(r'^[a-zA-Z0-9_]+$', text))

    # Extract hashtags from filtered tweets
    hashtags = []

    for tweet_obj in queryset:
        tweet_hashtags = tweet_obj.hashtags
        if tweet_hashtags:
            try:
                tweet_hashtags=ast.literal_eval(tweet_hashtags)
                if tweet_hashtags and len(tweet_hashtags)>0:
                    # Check if the tweet's language is English
                        print(tweet_hashtags)
                        print(tweet_obj.text)
                        if all(is_english(hashtag.strip('#')) for hashtag in tweet_hashtags):
                            hashtags.append(tweet_hashtags)
            except (SyntaxError,ValueError):
                pass

    # Filter out non-English hashtags
    # english_hashtags = []

    # for hashtags_list in hashtags:
    #     for hashtag in hashtags_list:
    #         try:
    #             if detect(hashtag) == 'en':
    #                 english_hashtags.append(hashtag)
    #         except:
    #             pass  
    # Construct output format
    #data = {'hashtags': hashtags}
     # Flatten the list of hashtags
    print("i m here")
    # Construct output format
    data = {'hashtags': hashtags}
    pair_counts = Counter()

    # Iterate over combinations of hashtags and count pairs
    for hash in data['hashtags']:
        pairs=combinations(hash,2)
        pair_counts.update(pairs)
        # print(pairs)
        # for i in pairs:
        #     if (detect(i)=="en"):
        #         pair_counts.update(pairs)
    # for hashtags_list in combinations(hashtags, 2):
    #     print(hashtags_list)
    #     if all(detect(hashtag) == 'en' for hashtag in hashtags_list):
    #         pair_counts.update([tuple(sorted(hashtags_list))])

    pair_counts_str_keys = {str(pair): count for pair, count in pair_counts.items()}

    # Sort the pair counts dictionary by count in decreasing order
    sorted_pair_counts = dict(sorted(pair_counts_str_keys.items(), key=lambda item: item[1], reverse=True))

    #Select only the top 50 items
    top_50_items = dict(list(sorted_pair_counts.items())[:50])

    print(type(sorted_pair_counts))
    return Response({'pair_counts': top_50_items})
   # new_data={}
    
    # for key,value in pair_counts_str_keys.items():
    #    newkey=ast.literal_eval(key)
    #    new_data[newkey]=value
    # print(new_data)
    
    # Construct response


   
  
    #df=pd.DataFrame(data)
    
#     return Response(result)

# def count_hashtag_combinations(hashtags_list):
#     ##  Counts the occurrences of each unique combination of hashtags
#     pairs = combinations(sorted(hashtags_list), 2)
    # return Counter(pairs)
#df['hashtag_combinations'] = df['hashtags'].apply(count_hashtag_combinations)
#print(df)
    
    
    
    
    
    
    
    
    
    
    
    
#     # Extract hashtags from tweets and generate pairs
#     hashtag_combinations = Counter()
#     for t in queryset:
#         hashtags = t.hashtags
#         pairs = itertools.combinations(sorted(hashtags), 2)
#         hashtag_combinations.update(pairs)
    
#     # Convert tuple keys to concatenated strings
#     hashtag_combinations_str_keys = {f"{tag1} {tag2}": count for (tag1, tag2), count in hashtag_combinations.items()}

#     return Response(hashtag_combinations_str_keys)

# def count_hashtag_combinations(hashtags_list):
#     ##  Counts the occurrences of each unique combination of hashtags
#     pairs = combinations(sorted(hashtags_list), 2)
#     return Counter(pairs)




        


#     # user_followers_count = scraped_tweets['user_followers_count'].iloc[i]
#                 # user_friends_count = scraped_tweets['user_friends_count'].iloc[i]
#                 # retweet_count = scraped_tweets['retweet_count'].iloc[i]
#                 # favorite_count = scraped_tweets['favorite_count'].iloc[i]
#                 # reach = scraped_tweets['reach'].iloc[i]
#                 # print("user_followers_count : ",user_followers_count)
