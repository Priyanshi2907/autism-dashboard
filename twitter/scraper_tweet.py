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
        "Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium",
        "Belize", "Benin","Bhutan", "Bolivia", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
        "Cambodia", "Cameroon",  "Canada",  "Cape Verde", "Central African Republic", "Chad", "Chile", "China",
        "Colombia","Comoros",     "Congo",        "Costa Rica",        "Croatia",        "Cuba",        "Cyprus",        "Czech Republic",        "Denmark",
        "Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea",
        "Estonia","Eswatini", "Ethiopia", "Fiji", "Finland", "France","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Grenada",
        "Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Ivory Coast","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati",
        "North Korea","South Korea","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania",
        "Luxembourg","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia",
        "Moldova","Monaco","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Zealand",
        "Nicaragua","Niger","Nigeria","North Macedonia","Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay",
        "Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Rwanda","Saint Kitts and Nevis","Saint Lucia","Samoa","San Marino","Saudi Arabia","Senegal","Serbia","Seychelles",
        "Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Sudan","Spain","Sri Lanka","Sudan","Suriname",
        "Sweden","Switzerland","Syria","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan",
        "Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela",
        "Vietnam","Yemen","Zambia","Zimbabwe","Abkhazia","Artsakh","Cook Islands","Kosovo","Niue","Northern Cyprus","Somaliland","South Ossetia",
        "Taiwan","Transnistria"]

# Dictionary mapping common aliases to full country names
country_aliases = {
    "usa": "United States", 
    "uk": "United Kingdom",
    "uae": "United Arab Emirates",
    
    # Add more aliases as needed
}

def extract_countries(text):
    """
    Extracts countries mentioned in the text of tweets.
    """
    mentioned_countries = []
    # Find all words in the text
    words = re.findall(r'\b\w+\b', text)
    # Check if each word matches any country or its alias in the 'countries' list
    for word in words:
        word_lower = word.lower()
        if word_lower in [country.lower() for country in countries]:
            mentioned_countries.append(word_lower.capitalize())  # Capitalize the first letter
        elif word_lower in [alias.lower() for alias in country_aliases.keys()]:
            mentioned_countries.append(country_aliases[word_lower.lower()])
    return mentioned_countries

#example
text="I love spain and albania"
mentioned_countires=extract_countries(text)
print(mentioned_countires)

related_keywords = [
    "health",
    "education",
    "Autism"
    #  "Asperger's syndrome",
    # "Autism spectrum disorder (asd)"
    # "Neurodevelopmental disorder",
    # "Social communication",
    # "Sensory processing",
    # "Behavioral therapy",
    # "Early intervention",
    # "Special education",
    # "Genetic factors",
    # "Neurodiversity",
    # "Social skills",
    # "Cognitive deficits",
    # "Speech therapy",
    # "Pervasive developmental disorder (PDD)",
    # "Executive function",
    # "Applied behavior analysis (ABA)",
    # "Communication difficulties",
    # "Repetitive behaviors",
    # "Hyperfocus",
    # "Inclusion", 
    # 'Autism Spectrum Disorder', 
    # 'Pervasive Developmental Disorder',
    # 'Autism Support', 
    # 'Autistic Children', 
    # 'Special Needs', 
    # 'Developmental Disability', 
    # 'Learning Disability',
    # 'Sensory Processing Disorder',
    # 'Social Skills Training'
    ]


def twitter_search(keyword):
    '''
    Searches for the Tweets with certain keyword  
    '''
    print("for ",keyword)
    url = "https://twitter154.p.rapidapi.com/search/search"
    
    today = datetime.today().strftime('%Y-%m-%d')
    # yesterday = today - timedelta(days=90)
    # yesterday = yesterday.strftime('%Y-%m-%d')
    
    # Increment the end_date by one day to include tweets for that day
    #end_date = end_date + timedelta(days=1)

    querystring = {
        "query": keyword,
        "section": "top",
        "start_date": today,
        "language": "en"
    }
    
    headers = {
    'X-RapidAPI-Key': 'a45e7c89f9msh9a3686ec4f10ddfp1232b7jsnbe301f7c1183',
    'X-RapidAPI-Host': 'twitter154.p.rapidapi.com'
  }
    
    response = requests.get(url, headers=headers, params=querystring)
    #response.raise_for_status()  # Raise an exception for HTTP errors
    print(response.json())
    try: 
        print("new here")
        data_2 = [{
            "tweet_id": tweet['tweet_id'],
            "text": tweet['text'],
            "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
            "tweet_link": tweet['expanded_url'],
            "user_screen_name": tweet['user']['username'],
            "user_followers_count": tweet['user'].get('follower_count', 0),  # Replace missing values with 0
            "username": tweet['user']['name'],
            "profile_pic":tweet['user']['profile_pic_url']
            } for tweet in response.json()['results'] 
            
            if all(tweet.get(key) for key in ['tweet_id', 'text', 'creation_date', 'expanded_url', 'user'])
            ]

    except Exception as e:
        data_2 = [{
            "tweet_id": tweet['tweet_id'],
            "text": tweet['text'],
            "created_at": datetime.strptime(tweet['creation_date'].replace('+0000', ''), "%a %b %d %H:%M:%S %Y").strftime('%Y-%m-%d'),
            "tweet_link": tweet['expanded_url'],
            "user_screen_name": tweet['user']['username'],
            "user_followers_count": tweet['user'].get('follower_count', 0),  # Replace missing values with 0
            "username": tweet['user']['username'],
            "profile_pic":tweet['user']['profile_pic_url']
            } for tweet in response.json()['results']
            
            if all(tweet.get(key) for key in ['tweet_id', 'text', 'creation_date', 'expanded_url', 'user','username','follower_count'])
        ]
    
    df = pd.DataFrame(data_2)
    print("i am comming here")       
    try:
            
            
        if "text" in df.columns:
            df['country']=df['text'].apply(extract_countries)
            df['country']=df["country"].apply(lambda x : ", ".join(x)) 
        else:
            df['country']=[]  
        if "user_screen_name" in df.columns:  
            df['user_profile_link'] = 'https://twitter.com/' + df['user_screen_name']    
        else:
            df['user_profile_link'] = " "
    except requests.exceptions.RequestException as e:
        print("Error is this ---", e)
        return None 
    
    # Sort the DataFrame by username in decreasing order of reach
    #df = df.sort_values(by=['user_followers_count'], ascending=False)

    # print("by reach : ",df)
    
    print ("df",type(df))
    print(df)
       
    return df #hashtags_count
    



def main():
    # main_df = pd.DataFrame()
   
    for related_keyword in related_keywords:
    
        # for country in countries:        
    
            keyword = related_keyword 
  
            print("keyword in main : ",keyword)
            output = twitter_search(keyword)
            
            
        # main_df = pd.concat([main_df, df], axis=0)
        
    # main_df.reset_index(drop=True, inplace=True)      

    # main_df
#main()