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
from lxml_html_clean import clean_html
import google.generativeai as genai
from selenium.common.exceptions import WebDriverException

driver=webdriver.Chrome()  
#driver = webdriver.Chrome()
GOOGLE_API_KEY= 'AIzaSyAEgGg08BmZIDyxOiCVeRlibO9OTOLxTMs'

# try:
#     driver = webdriver.Chrome()
# except WebDriverException as e:    
#     time.sleep(10)  # Wait for 10 seconds before attempting to reconnect    
#     driver = webdriver.Chrome()  # Reinitialize the WebDriver
         
countries = [
         "Afghanistan"]
        #  "Albania",
        #  "Algeria",
        # "Andorra","Angola","Antigua and Barbuda","Argentina","Armenia",]
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
           
related_keywords = [
    "health"
    # "Autism",
    # "Asperger's syndrome",
    # "Autism spectrum disorder (asd)",
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

def headlines(link):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    link.strip()
    page = Article(str(link), config=config)
    try:
        # print('title page')
        page.download()
        page.parse()
        return page.title
    except:
        # print("untitled page")
        return 'Untitled Page'

ll = []
def google_news_scraper(keyword):
    print("i am here")
    
    # Calculate the date 15 days ago
    #fifteen_days_ago = datetime.now() - timedelta(days=30)

    for j in range(0,20,10):
        link = f'https://www.google.co.in/search?q={keyword}+news&sca_esv=64568e91d4c772e8&tbm=nws&prmd=nivsmbtz&sxsrf=ACQVn0-qaS0objyOU3CfpFe1WOR3BQfJHw:1712395312013&ei=MBQRZoQ06-6x4w_n_4nQDA&start={j}&sa=N&ved=2ahUKEwiEjKbSoa2FAxVrd2wGHed_Aso4RhDy0wN6BAgDEAQ&biw=1536&bih=695&dpr=1.25'
        #link = 'https://www.google.com/search?q='+str(keyword) +' '+'news'
        
        ll.append(link)
    

    data = []
    visited_urls = set()
    visited_url_date=set()
    for link in ll:  
        driver.get(link)
        driver.implicitly_wait(5)
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        news = soup.find_all("div",attrs={'class':"SoaBEf"})
        for row in news:
            des = {}
            
            title = row.find('div',attrs={'class':"n0jPhd ynAwRc MBeuO nDgy9d"}).text
            url = row.find("a",attrs={'class':"WlydOe"}).get('href')
            
            source = row.find('div',attrs={'class':"MgUUmf NUnG9d"}).text
            date = row.find('div',attrs={'class':"OSrXXb rbYSKb LfVVr"}).text
            
             # Parse the date string into a datetime object
            #article_date = dateparser.parse(date)
            # images = row.find('img').get('src')
            # Check if the article is from today
            #if article_date.date() >= datetime.now().date():
            images = row.find('img').get('src')
            if url not in visited_urls and date not in visited_url_date:
                des['source'] = source
                des['link'] = url
                des['title'] = title
                des['date'] = date
                des['image'] = images
                data.append(des)
                #print("data: ",data)
                visited_urls.add(url)
    # df=pd.DataFrame(data)
    # keyCountry=keyword.split()
    # df['country']=keyCountry[-1]
    #print(df)
    #return df
    
                    #print("+++",visited_urls)

    today = datetime.today().strftime('%Y-%m-%d')
    # yesterday = today - timedelta(days=30)
    # yesterday = yesterday.strftime('%Y-%m-%d')
    

    DATE = []  
    for i in data:
        if i['date']:
            date = dateparser.parse(i['date'])
        if date:
            date = date.strftime("%Y-%m-%d")
            DATE.append(date)
            print("Date: ",DATE)

        # article_date = dateparser.parse(article['date'])
        # if article_date and article_date.date() == (datetime.now() - timedelta(days=1)).date():
        #     filtered_data_final.append(article)

    filtered_data = []
    for data1, modified_date in zip(data, DATE):
        if modified_date:
            data1['Modified Dates'] = modified_date
            filtered_data.append(data1)
            #print(filtered_data)

    filtered_data_final = []
    for data2 in filtered_data:
        if data2['Modified Dates']:
            modified_date = dateparser.parse(data2['Modified Dates'], date_formats=['%Y-%m-%d'])
            modified_date = modified_date.strftime('%Y-%m-%d')
            # if modified_date == today:
            if modified_date == today:
                filtered_data_final.append(data2)
                print("filter dta : ",filtered_data_final)
    list1 = []
    for item in filtered_data_final:
        title = item['title']
        if detect(title) == 'en':  
            list1.append(item)  

    for item in list1:
        item['title'] = headlines(item['link']) 

    list1 = [x for x in list1 if isinstance(x, dict) and x.get('title') is not None and ('Error' not in x['title']) and ('Captcha' not in x['title']) and
             ('Are you a robot?' not in x['title']) and ('Untitled Page' not in x['title']) and 
             ('Subscribe' not in x['title']) and ('You are being redirected...' not in x['title']) and 
             ('Not Acceptable!' not in x['title']) and ('403 Forbidden' not in x['title']) and 
             ('ERROR: The request could not be satisfied' not in x['title']) and ('Just a moment...' not in x['title']) and 
             ('403 - Forbidden: Access is denied.' not in x['title']) and ('Not Found' not in x['title']) and 
             ('Page Not Found' not in x['title']) and ('StackPath' not in x['title']) and ('Access denied' not in x['title'])
             and ('Yahoo' not in x['title']) and ('Stock Market Insights' not in x['title']) and 
             ('Attention Required!' not in x['title']) and ('Access Denied' not in x['title'])
             and ('403 forbidden' not in x['title']) and ('Too Many Requests' not in x['title'])
             and ('403 - Forbidden' not in x['title']) and ('NCSC' not in x['title'])
             and ('BC Gov News' not in x['title']) and ('The Verge' not in x['title']) and ('Trackinsight' not in x['title'])
             and ('Morning Headlines' not in x['title']) and ('Forbidden' not in x['title'])
             and ('forbidden' not in x['title']) and ('Detroit Free Press' not in x['title'])
             and ('reuters.com' not in x['title']) and ('403 unauthorized' not in x['title'])
             and ('403 not available now' not in x['title']) and ('Not Acceptable' not in x['title']) 
             and ('Your access to this site has been limited by the site owner' not in x['title'])
             and ('404 - File or directory not found.' not in x['title'])]

    for item in list1:
        if 'Fortune India: Business News, Strategy, Finance and Corporate ...' in item['source']:
            item['source'] = 'Fortune India'
    print("list1 :",list1)
    df=pd.DataFrame(list1)
    keyCountry=keyword.split()
    df['country']=keyCountry[-1]
    return df

def take_keyword():
    for relatedkeyword in related_keywords:
        for country in countries:
            keyword=relatedkeyword+" "+country
            print(f'\n Fetching News articles for- {keyword} news\n')
            data = google_news_scraper(keyword)
            df=pd.DataFrame(data)
            print(df)
            
#take_keyword()