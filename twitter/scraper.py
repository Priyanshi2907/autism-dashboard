# scraper.py

import requests 
from datetime import datetime, timedelta
import pandas as pd
import re 
related_keywords = [
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

def twitter_search(keyword):
    '''
    Searches for the Tweets with certain keyword  
    '''
    url = "https://twitter154.p.rapidapi.com/search/search"
    
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    
    querystring = {
        "query": keyword,
        "section": "top",
        "min_retweets": "1",
        "min_likes": "1",
        "limit": "20",
        "start_date": yesterday,
        "language": "en"
    }
    
    headers = {	
        'X-RapidAPI-Key': 'f7173b49d5msh09de40987862b60p194beajsn834236db5d67',
        'X-RapidAPI-Host': 'twitter154.p.rapidapi.com'
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data_2 = [{
            "tweet_id": tweet['tweet_id'],
            "text": tweet['text'],
            "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
            "tweet_link": tweet['expanded_url'],
            "user_screen_name": tweet['user']['username'],
            "user_location": tweet['user']['location'],
            "user_followers_count": tweet['user']['follower_count'],
            "user_friends_count": tweet['user']['following_count'],
            "retweet_count": tweet['retweet_count'],
            "favorite_count": tweet['favorite_count'],
            "lang": tweet['language']
        } for tweet in response.json()['results']]

        df = pd.DataFrame(data_2)

        df['reach'] = df['user_followers_count'] + df['user_friends_count'] + df['retweet_count'] + df['favorite_count']
        # Apply the lambda function to each row of the DataFrame
        df['hashtags'] = df['text'].apply(lambda x: re.findall(r'#\w+', x))

        hashtags_count = {}
        hashtags = [hashtag for hashtag_list in df['hashtags'] for hashtag in hashtag_list]
        for i in hashtags:
            if i in hashtags_count:
                hashtags_count[i] += 1
            else:
                hashtags_count[i] = 1
        print(hashtags_count)
        print (df)
        return df, hashtags_count
    
        

        #return data_2
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None  # Return None to indicate failure
    
df, hashtags_count = twitter_search('health')

# def getresponse():
#     keyword=input("Enter keyword : ")
#     country=input("enter country : ")
    
#     print(f'\n Fetching the tweets for- {keyword} \n')

#     df_twitter=twitter_search(keyword)
#     print(df_twitter)

#     return df_twitter

# getresponse()
