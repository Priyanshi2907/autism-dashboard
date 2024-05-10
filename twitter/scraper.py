# scraper.py

import requests 
from datetime import datetime, timedelta
import pandas as pd
import re 
import spacy
import google.generativeai as genai
from itertools import combinations
from collections import Counter


GOOGLE_API_KEY= 'AIzaSyAEgGg08BmZIDyxOiCVeRlibO9OTOLxTMs'
# list of countries
countries = [
       
          "Afghanistan","Albania","Algeria",
        "Andorra","Angola","Antigua and Barbuda","Argentina","Armenia",
        "Australia","Austria","Azerbaijan","Bahamas, The","Bahrain","Bangladesh","Barbados","Belarus","Belgium",
        "Belize", "Benin","Bhutan", "Bolivia", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
        "Cambodia", "Cameroon",  "Canada",  "Cape Verde", "Central African Republic", "Chad", "Chile", "China"]
        # "Colombia","Comoros",     "Congo",        "Costa Rica",        "Croatia",        "Cuba",        "Cyprus",        "Czech Republic",        "Denmark",
        # "Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea",
        # "Estonia","Eswatini", "Ethiopia", "Fiji", "Finland", "France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada",
        # "Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Ivory Coast","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati",
        # "North Korea","South Korea","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania",
        # "Luxembourg","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia",
        # "Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand",
        # "Nicaragua","Niger","Nigeria","North Macedonia","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay",
        # "Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia","Samoa","San Marino","Saudi Arabia","Senegal","Serbia","Seychelles",
        # "Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Sudan","Spain","Sri Lanka","Sudan","Suriname",
        # "Sweden","Switzerland","Syria","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan",
        # "Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela",
        # "Vietnam","Yemen","Zambia","Zimbabwe","Abkhazia","Artsakh","Cook Islands","Kosovo","Niue","Northern Cyprus","Somaliland","South Ossetia",
        # "Taiwan","Transnistria"]

related_keywords = [
    # "health",
                    # "education",
     "Asperger's syndrome",
    "Autism spectrum disorder (asd)"
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
# Sample Data
data = {'hashtags': [
        ['health', 'autism'],
        ['autism', 'inclusion'],
        ['health', 'autism'],
        ['health', 'autism'],
        ['health', 'disability', 'autism'],
        ['health', 'inclusion', 'disability','autism']
        
    ]}
df = pd.DataFrame(data)

def count_hashtag_combinations(hashtags_list):
    ##  Counts the occurrences of each unique combination of hashtags
    pairs = combinations(sorted(hashtags_list), 2)
    return Counter(pairs)
df['hashtag_combinations'] = df['hashtags'].apply(count_hashtag_combinations)

#print(df)

total_combined_counter = sum(df['hashtag_combinations'], Counter())

individual_counters = [Counter({pair: count}) for pair, count in total_combined_counter.items()]

# for counter in individual_counters:
#     print(counter)

# Apply the function to the 'hashtags' column
# df['hashtag_combinations'] = df['hashtags'].apply(count_hashtag_pairs)
# display(df)

# total_combined_counter = sum(df['hashtag_combinations'], Counter())

# individual_counters = [Counter({pair: count}) for pair, count in total_combined_counter.items()]

# for counter in individual_counters:
#         print(counter)




nlp = spacy.load("en_core_web_sm")

# def NER(text):
    
#     doc = nlp(text)
    
#     orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
#     person = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
#     print("in NER orgs",orgs) 
#     print("in NER person",person)   
#     return orgs, person

def NER(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities.append("org")
        elif ent.label_ == "PERSON":
            entities.append("person")
        
    if entities:
        print("In ner :",entities[0])
        return entities[0]
    else:
        return "all"

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
def twitter_search(keyword):
    
    
            
    '''
    Searches for the Tweets with certain keyword  
    '''
    print("for ",keyword)
    url = "https://twitter154.p.rapidapi.com/search/search"
    
    today = datetime.today()
    yesterday = today - timedelta(days=90)
    yesterday = yesterday.strftime('%Y-%m-%d')
    
    # Increment the end_date by one day to include tweets for that day
    #end_date = end_date + timedelta(days=1)

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
    'X-RapidAPI-Key': 'ede002137bmsh8b276e5911da552p104e91jsn05192d4dc026',
    'X-RapidAPI-Host': 'twitter154.p.rapidapi.com'
  }
    ## Country Wise Calculation
    country_positive_counts = {}
    country_negative_counts = {}

    
    response = requests.get(url, headers=headers, params=querystring)
    #response.raise_for_status()  # Raise an exception for HTTP errors
    print(response.json())
    try: 
        # tweets_data = response.json()['results']
        # if not tweets_data:
        #     print("No tweets found.")
        #     return None
        data_2 = [{
            "tweet_id": tweet['tweet_id'],
            "text": tweet['text'],
            "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
            "tweet_link": tweet['expanded_url'],
            "user_screen_name": tweet['user']['username'],
            "user_location": tweet['user']['location'],
            "user_followers_count": tweet['user'].get('follower_count', 0),  # Replace missing values with 0
            "user_friends_count": tweet['user'].get('following_count', 0),  # Replace missing values with 0
            "retweet_count": tweet.get('retweet_count', 0),  # Replace missing values with 0
            "favorite_count": tweet.get('favorite_count', 0), 
            "lang": tweet['language'],
            "username": tweet['user']['name']
            } for tweet in response.json()['results'] ]

    except Exception as e:
        data_2 = [{
            "tweet_id": tweet['tweet_id'],
            "text": tweet['text'],
            "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
            "tweet_link": tweet['expanded_url'],
            "user_screen_name": tweet['user']['username'],
            "user_location": tweet['user']['location'],
            "user_followers_count": tweet['user'].get('follower_count', 0),  # Replace missing values with 0
            "user_friends_count": tweet['user'].get('following_count', 0),  # Replace missing values with 0
            "retweet_count": tweet.get('retweet_count', 0),  # Replace missing values with 0
            "favorite_count": tweet.get('favorite_count', 0), 
            "lang": tweet['language'],
            "username": tweet['user']['username'],
            } for tweet in response.json()['results']]
    
    df = pd.DataFrame(data_2)
    print("i am comming here")
    
       
    try:
            
            
            if 'user_followers_count' in df.columns and 'text' in df.columns:
                df['reach'] = df['user_followers_count'] + df['user_friends_count'] + df['retweet_count'] + df['favorite_count']
                df['hashtags'] = df['text'].apply(lambda x: re.findall(r'#\w+', x))

                df['sentiment'] = df['text'].apply(sentiment)
    
                keyCountry=keyword.split()
                df['country'] = keyCountry[-1]
     
                df['entity']=df["username"].apply(NER)
    
                df['user_profile_link'] = 'https://twitter.com/' + df['user_screen_name']
    
            else:
                df['reach'] = 0
                df["hashtags"]=[]
                df['sentiment'] = " "
    
                keyCountry=keyword.split()
                df['country'] = " "
     
                df['entity']=" "
    
                df['user_profile_link'] = " "

            
            
            # hashtags_count = {}
            # hashtags = [hashtag for hashtag_list in df['hashtags'] for hashtag in hashtag_list]
            # for i in hashtags:
            #     if i in hashtags_count:
            #         hashtags_count[i] += 1
            #     else:
            #         hashtags_count[i] = 1
    
        
        # print("hashtag_count : ",hashtags_count)
    except requests.exceptions.RequestException as e:
        print("Error is this ---", e)
        return None 
    
    # Sort the DataFrame by username in decreasing order of reach
    df = df.sort_values(by=['reach'], ascending=False)

    print("by reach : ",df)
    
    print ("df",type(df))
    print(df)
    

    
    return df #hashtags_count
    
    
        

        #return data_2
     # Return None to indicate failure
# for related_keyword in related_keywords:     
#     df, hashtags_count = twitter_search(related_keyword)

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


def main():
    main_df = pd.DataFrame()
   
    for related_keyword in related_keywords:
    
        for country in countries:        
    
            keyword = related_keyword + ' ' + country
  
            print("keyword in main : ",keyword)
            output = twitter_search(keyword)
            #if output is not None:
             #   filtered_tweets = filter_tweets_by_month(output)
              #  positive_count, negative_count = count_sentiment(filtered_tweets)
               # print("Total positive tweets for current month:", positive_count)
                #print("Total negative tweets for current month:", negative_count)

            #print("main df : ",output)
        
        # if not df.empty:
        # df['country'] = country
            
        # main_df = pd.concat([main_df, df], axis=0)
        
    main_df.reset_index(drop=True, inplace=True)      

    main_df
main()