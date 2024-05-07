import requests 
from datetime import datetime, timedelta
import pandas as pd
import re 
import spacy
import google.generativeai as genai
from itertools import combinations
from collections import Counter
#from . scraper import *
#from news.scraper import *

GOOGLE_API_KEY= 'AIzaSyAEgGg08BmZIDyxOiCVeRlibO9OTOLxTMs'

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
genai.configure(api_key=GOOGLE_API_KEY)

    
generation_config = {
  "candidate_count": 1,
  "max_output_tokens": 256,
  "temperature": 1.0,
  "top_p": 0.7,
}

safety_settings=[
  {
    "category": "HARM_CATEGORY_DANGEROUS",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
#     generation_config=generation_config,
    safety_settings=safety_settings
)
def sentiment(text):
    """
    Fetches Sentiment from the given text
    """
    try:

        response = model.generate_content(f"""
  
            You are a helpful assistant that can analyze the text and analyze Sentiment 
            
            Understand and Identify the Sentiment for the following text: {text}
            
            Output should contain only 'Positive' , 'Negative' or 'Neutral'.
            
            """)

        return response.text
    
    # except:
    except Exception as e:
        print(e)
        return 'No Response'

related_keywords = ["sports"]
countries=["india"]
def twitter_search_present(keyword):            
    '''
    Searches for the Tweets with certain keyword  
    '''
    print("for present tweet ",keyword)
    url = "https://twitter154.p.rapidapi.com/search/search"
    
    today = datetime.today()
    today=today.strftime('%Y-%m-%d')
    # yesterday = today - timedelta(days=1)
    # yesterday = yesterday.strftime('%Y-%m-%d')
    
    # Increment the end_date by one day to include tweets for that day
    #end_date = end_date + timedelta(days=1)

    querystring = {
        "query": keyword,
        "section": "top",
        "min_retweets": "1",
        "min_likes": "1",
        "limit": "20",
        "start_date": today,
        "language": "en"
    }
    
    headers = {
    'X-RapidAPI-Key': 'ede002137bmsh8b276e5911da552p104e91jsn05192d4dc026',
    'X-RapidAPI-Host': 'twitter154.p.rapidapi.com'
  }
    
    response = requests.get(url, headers=headers, params=querystring)
    #response.raise_for_status()  # Raise an exception for HTTP errors
    #print(response.json())
    try:
         
         data_2=[{
            "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
            "text": tweet['text'], 
         } for tweet in response.json()['results']]
    except Exception as e:
         print ("Error : ",e)
    df=pd.DataFrame(data_2)
      
    try:

         df['sentiment'] = df['text'].apply(sentiment)
         print(df)
                      
    except requests.exceptions.RequestException as e:
        print("Error is this ---", e)
        return None
    
def twitter_search_yesterday(keyword):

    '''
    Searches for the Tweets with certain keyword  
    '''
    print("for yesterday tweet ",keyword)
    url = "https://twitter154.p.rapidapi.com/search/search"
    
    
    yesterday = datetime.today() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    

    # start_date = f"{yesterday_str}T00:00:00Z"
    # end_date = f"{yesterday_str}T23:59:59Z"

    querystring = {
        "query": keyword,
        "section": "top",
        "min_retweets": "0",
        "min_likes": "0",
        "limit": "15",
        "start_date": yesterday_str,
        "end_date": yesterday_str,
        "language": "en"
    }
    
    headers = {
    'X-RapidAPI-Key': 'ede002137bmsh8b276e5911da552p104e91jsn05192d4dc026',
    'X-RapidAPI-Host': 'twitter154.p.rapidapi.com'
  }
    
    response = requests.get(url, headers=headers, params=querystring)
    #response.raise_for_status()  # Raise an exception for HTTP errors
    #print(response.json())
    try:
         
         data_2=[{
            "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
            "text": tweet['text'], 
         } for tweet in response.json()['results']]
    except Exception as e:
         print ("Error : ",e)
    df=pd.DataFrame(data_2)
      
    try:
        if 'text' in df.columns:
            df['sentiment'] = df['text'].apply(sentiment)
        else:
            df['sentiment']=" "
        print(df)
                      
    except requests.exceptions.RequestException as e:
        print("Error is this ---", e)
        return None

def main():
    for related_keyword in related_keywords:
    
        for country in countries:        
    
            keyword = related_keyword + ' ' + country
  
            print("keyword in main : ",keyword)
            #output_present_tweet = twitter_search_present(keyword)
            output_yesterday_tweet=twitter_search_yesterday(keyword)

main()
   
    
   