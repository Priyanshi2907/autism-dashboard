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

driver = webdriver.Chrome()
ll=[]
for j in range(0,100,10):
        link = 'https://www.google.co.in/search?q=real+estate+gurgaon+news&sca_esv=64568e91d4c772e8&tbm=nws&prmd=nivsmbtz&sxsrf=ACQVn0-qaS0objyOU3CfpFe1WOR3BQfJHw:1712395312013&ei=MBQRZoQ06-6x4w_n_4nQDA&start='+str(j)+'&sa=N&ved=2ahUKEwiEjKbSoa2FAxVrd2wGHed_Aso4RhDy0wN6BAgDEAQ&biw=1536&bih=695&dpr=1.25'
        driver.implicitly_wait(5)
        ll.append(link)
    
    
data=[]
for link in range(len(ll)):  
    URL = ll[link]
    driver.get(URL)
    driver.implicitly_wait(5)
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    
    news = soup.find_all("div",attrs={'class':"SoaBEf"})
    
    for row in news:
        des={}
        driver.implicitly_wait(5)
        title =  row.find('div',attrs={'class':"n0jPhd ynAwRc MBeuO nDgy9d"}).text
        
        driver.implicitly_wait(5)
        url=row.find("a",attrs={'class':"WlydOe"})
        link=url.get('href')
        
        driver.implicitly_wait(5)
        source =  row.find('div',attrs={'class':"MgUUmf NUnG9d"}).text
        
        driver.implicitly_wait(5)
        date =  row.find('div',attrs={'class':"OSrXXb rbYSKb LfVVr"}).text

        driver.implicitly_wait(5)
        images =  row.find('img')
        image = images.get('src')
        
        des['source']=source
        des['link']=link
        des['title']=title
        des['date']=date
        des['image']=image
        data.append(des)

# This function takes a news link as input and returns the headline of the news. 
    # It uses the newspaper module to extract the headline.
def headlines(link):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    link.strip()
    page = Article(str(link), config=config)
    try:
        page.download()
        page.parse()
        return page.title
    except:
        return 'Untitled Page'



# The handle method first obtains the current date and then calculates the date of yesterday. 
    # It uses the datetime module to achieve this.
    #now = date.today()
    
now = datetime.now()
now = now.date()
yesterday = now - timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')

y = []

# The code then processes the scraped news data by extracting the date of each article and filtering out any articles that 
# are not from the previous day. 
DATE = []
for i in data:
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


    filtered_data_final = []
    for data2 in filtered_data:
        if data2['Modified Dates']:
            modified_date = dateparser.parse(data2['Modified Dates'], date_formats=['%Y-%m-%d'])
            modified_date = modified_date.strftime('%Y-%m-%d')
            if modified_date == yesterday:
                filtered_data_final.append(data2)
                


# It filters out any articles that are not in English.
list1 = []
for item in filtered_data_final:
    title = item['title']
    if detect(title) == 'en':  
        list1.append(item)  

# This fetches the headline if number of words>10.
for item in list1:
    item['title'] = headlines(item['link']) 
        

# # Removes news of the given title
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
#          and ('403 - Forbidden' not in x['title']) and ('NCSC' not in x['title'])
#          and ('BC Gov News' not in x['title']) and ('The Verge' not in x['title']) and ('Trackinsight' not in x['title'])
#          and ('Morning Headlines' not in x['title']) and ('Forbidden' not in x['title'])
#          and ('forbidden' not in x['title']) and ('Detroit Free Press' not in x['title'])
#          and ('reuters.com' not in x['title']) and ('403 unauthorized' not in x['title'])
#          and ('403 not available now' not in x['title']) and ('Not Acceptable' not in x['title']) 
#          and ('Your access to this site has been limited by the site owner' not in x['title'])
#          and ('404 - File or directory not found.' not in x['title'])]


# # # Changing the this relevant source name
# for item in list1:
#     if 'Fortune India: Business News, Strategy, Finance and Corporate ...' in item['source']:
#         item['source'] = 'Fortune India'



# Extend the all_data list with the current list1
y.extend(list1)
df = pd.DataFrame(y)
print(df)