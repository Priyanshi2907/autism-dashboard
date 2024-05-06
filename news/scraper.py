import urllib.request,sys,time
from bs4 import BeautifulSoup
from datetime import timedelta
import requests
import json
from selenium import webdriver
import re
from newspaper import Article
from newspaper import Config
import dateparser
from langdetect import detect
from datetime import datetime, timedelta, date
import pandas as pd
import google.generativeai as genai
from collections import defaultdict



# Example DataFrame\n",
df = pd.DataFrame({'A': [1, 2, 3]})#, 'B': [4, 5, 6]})\n",
# Reset index,
df.reset_index(drop=True, inplace=True)
# Print DataFrame without indices and without the default integer index column\n",
df = df.to_string(index=False)

print(df)
# Pass your Gemini API key here 
GOOGLE_API_KEY= 'AIzaSyAEgGg08BmZIDyxOiCVeRlibO9OTOLxTMs'


# list of countries
    
countries = [
         "Afghanistan","Albania"]#"Algeria",]
        #"Andorra","Angola","Antigua and Barbuda","Argentina","Armenia",
        # "Australia","Austria","Azerbaijan","Bahamas, The","Bahrain","Bangladesh","Barbados","Belarus","Belgium",
        # "Belize", "Benin","Bhutan", "Bolivia", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
        # "Cambodia", "Cameroon",  "Canada",  "Cape Verde", "Central African Republic", "Chad", "Chile", "China",
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

#list of keywords
related_keywords = [
    "Asperger's syndrome",
    "Autism spectrum disorder (asd)"
    #"Neurodevelopmental disorder",
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
    
# This fuction takes a URL as input and returns a news link from Google News. 
# It uses the requests and BeautifulSoup modules to extract the link.
def find_news_link(URL11):
    page=requests.get(URL11,timeout=20)
    soup11 = BeautifulSoup(page.content, 'html.parser')
    result11 = soup11.find('div', {'class':'Pg70bf Uv67qb'})
    links = result11.find_all('a', {'class':'eZt8xd'})
    link_list = links[0]['href']
    return "https://www.google.com/"+link_list


# This function takes a news URL as input and returns a list of dictionaries that contain news data such as source, link, title, and date. 
# It uses the requests and BeautifulSoup modules to extract the data. It also uses a loop to fetch data from multiple pages of Google News.
def find_news_data(url):
    URL = find_news_link(url)
    page=requests.get(URL,timeout=20)

    final_list=[]
    page_num = 0
    while page_num < 1:
        page_num += 1
        print(f"{page_num} page:")
        soup11 = BeautifulSoup(page.content, 'html.parser')

        # print(soup11)
        
        result = soup11.find_all('div', {'class':'Gx5Zad fP1Qef xpd EtOod pkphOe'})#Gx5Zad xpd EtOod pkphOe #Gx5Zad fP1Qef xpd EtOod pkphOe

        # print(result[0])

        for i in result:
            des={}
            source = i.find('div', {'class':'BNeawe UPmit AP7Wnd lRVwie'}).text
            link = i.find('a')['href'].replace('/url?q=','')
            title = i.find('h3').text
            description = i.find('div', {'class': 'BNeawe s3v9rd AP7Wnd'}).text
            date_element = i.find('span', {'class': 'r0bn4c rQMQod'})
            if date_element:
                date = date_element.text
                des['date'] = date
            else:
                des['date'] = None
            final_link = link.split('&')[0]
            
            # news = requests.get(final_link)
            # soup_news = BeautifulSoup(news.content, 'html.parser')

            # print(soup_news)
            # print('-'*40)
            
            # image_link = i.find('img')['src']
            

            des['source']=source
            des['link']=final_link
            des['title']=title
           # des['date']=date
            des['description'] = description

            # des['image_link'] = image_link
            
            # des['description']=headlines(final_link)[1]  # gets the description of the mews article
            # des['summary'] = headlines(final_link)[2]
            final_list.append(des)
        
        try:
            next_link = soup11.find('a', {'aria-label':'Next page'})['href']


            URL1='https://www.google.com/'+next_link
            page=requests.get(URL1,timeout=20)
            print(URL1)
        except Exception as e:
            print("Error:", e)
            break        
    return final_list,soup11
    # time.sleep(1)


# This function takes a news link as input and returns the headline of the news. 
# It uses the newspaper module to extract the headline and description of the article.
def headlines(link):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    link.strip()
    page = Article(str(link), config=config)
    try:
        page.download()
        page.parse()
        return page.title, page.text #, page.summary
    except:
        return 'Untitled Page'


# This function takes a URL as input and returns the title of the webpage. (used if the number of words in headline>10) 
# It uses the requests and BeautifulSoup modules to extract the title.
def get_page_title(url):
    try:
        r = requests.get(url,timeout=20)
        soup = BeautifulSoup(r.content, "html.parser")
        if soup.title and soup.title.text:
            return soup.title.text
        else:
            return "Error"
    except requests.exceptions.Timeout:
        return "Error"
    except requests.exceptions.RequestException:
        return None




def google_news_scraper(keyword,start_date, end_date):
    print("Keyyyywordd is this:",keyword)
    
    ##Country wise Calculation
    # Initialize dictionary to store counts for each country
    country_counts = defaultdict(lambda: {'positive': 0, 'negative': 0})



    # It constructs a Google search URL by concatenating the keyword and industry category, 
    # and then it passes this URL to the find_news_data function to scrape the news data from the Google search results page.
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    URL = f'https://www.google.com/search?q={keyword}+news&tbm=nws&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{start_date_str}%2Ccd_max%3A{end_date_str}'
    # print(URL)
    
    y=[]

    data ,soup11 = find_news_data(URL)
    user_agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    print("*"*50)                  
    # print(data)
   
    for item in data:
         #sentiment = get_sentiment(item['description'])
        sentiments = sentiment(item['description'])
        
        
        # Extract country from the news data
        keyCountry=keyword.split()
        countryname = keyCountry[-1]
        
         # Update counts based on sentiment
        if sentiments == 'Positive':
            country_counts[countryname]['positive'] += 1
        elif sentiments == 'Negative':
            country_counts[countryname]['negative'] += 1
      # Print country-wise counts
    for countryname, counts in country_counts.items():
        print(f"Country: {countryname}")
        print(f"Positive News Count: {counts['positive']}")
        print(f"Negative News Count: {counts['positive']}")
        print("Total Count : ",counts['positive']+counts['positive'])
        print()


    # The code then processes the scraped news data by extracting the date of each article and filtering out any articles that 
    # are not from the previous day. 
    DATE = []
    for i in data:
        date=None
        if i['date']:
            date = dateparser.parse(i['date'])
        if date:
            date = date.strftime("%Y-%m-%d")
            DATE.append(date)

    filtered_data = []
    
    for data1, modified_date in zip(data, DATE):
        if modified_date:
            data1['Modified Dates'] = modified_date
            filtered_data.append(data1)



    # It filters out any articles that are not in English.
    list1 = []
    for item in filtered_data:
        # title = item['title']
        # if detect(title) == 'en':  
        list1.append(item)     


    # # This fetches the headline if number of words>10.
    for item in list1:
        # if len(item['title'].split()) > 10:
        item['title'] = get_page_title(item['link'])
        # else:
        #     item['title'] = headlines(item['link'])       

    # Removes news of the given title
    # list1 = [x for x in list1 if isinstance(x, dict) and x.get('title') is not None and ('Error' not in x['title']) and ('Captcha' not in x['title']) and
    #          ('Are you a robot?' not in x['title']) and ('Untitled Page' not in x['title']) and 
    #          ('Subscribe' not in x['title']) and ('You are being redirected...' not in x['title']) and 
    #          ('Not Acceptable!' not in x['title']) and ('403 Forbidden' not in x['title']) and 
    #          ('ERROR: The request could not be satisfied' not in x['title']) and ('Just a moment...' not in x['title']) and 
    #          ('403 - Forbidden: Access is denied.' not in x['title']) and ('Not Found' not in x['title']) and 
    #          ('Page Not Found' not in x['title']) and ('StackPath' not in x['title']) and ('Access denied' not in x['title'])
    #          and ('Yahoo' not in x['title']) and ('Stock Market Insights' not in x['title']) and 
    #          ('Attention Required!' not in x['title']) and ('Access Denied' not in x['title'])
    #          and ('403 forbidden' not in x['title']) and ('Too Many Requests' not in x['title'])
    #          and ('403 not available now' not in x['title']) and ('Not Acceptable' not in x['title']) 
    #          and ('Your access to this site has been limited by the site owner' not in x['title'])
    #          and ('404 - File or directory not found.' not in x['title'])]

    


    # Extend the all_data list with the current list1
    y.extend(list1)
    df = pd.DataFrame(y)
    df['sentiment'] = df['description'].apply(sentiment)
    keyCountry=keyword.split()
    df['country']=keyCountry[-1]
    print(df)
    return df


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


        

    
# def right_relevance():

#     main_df = pd.DataFrame()

#     for related_keyword in related_keywords:
#         for country in countries:
#             keyword = related_keyword+' '+ country
#             #print(keyword)
#             print(f'\n Fetching News articles for- {keyword} news\n')
#             df = google_news_scraper(keyword)
#             #print("sentiments")
#             df['sentiment'] = df['description'].apply(sentiment)
               
#             # print(df)
#             df['country']=country
#             
            
#             main_df=pd.concat([main_df,df],axis=0)
#     main_df.reset_index(drop=True,inplace=True)
#     return main_df

    
    
    # print(df)
    # return df

# df=right_relevance()
#df
# keyword = input('Enter the Keyword: ')

    # country = input('Kindly enter the country to access articles relevant to its region: ')
    
# def count_sentiment():
#     # Filter the data for the current month
#     current_month = datetime.now().strftime("%Y-%m")
#     df_current_month = df[df["date"].str.contains(current_month)]
    
#     # Apply sentiment analysis to the text of each news article
#     df_current_month["sentiment"] = df_current_month["text"].apply(sentiment)
    
#     # Check the type of the sentiment data
#     print(type(df_current_month["sentiment"]))
    
#     # If the sentiment data is a string, access its characters using integer indices
#     if isinstance(df_current_month["sentiment"], str):
#         positive_count = sum(1 for sentiment in df_current_month["sentiment"] if sentiment[0] == "p")
#         negative_count = sum(1 for sentiment in df_current_month["sentiment"] if sentiment[0] == "n")
    
#     print(f"Positive news count: {positive_count}")
#     print(f"Negative news count: {negative_count}")


# count_sentiment()