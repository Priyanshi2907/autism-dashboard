from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import News
from .serializers import NewsSerializers
from .scraper import *
from django.db import transaction
# Create your views here.

class SearchNews(APIView):
    def get(self, request):
        related_keywords = ["Autism spectrum disorder (asd)","Asperger's syndrome"]
        countries = ["Albania","Afghanistan"]        
        for related_keyword in related_keywords:
            for country in countries:
                keyword = related_keyword+' '+ country
                print("keyword from view : ",keyword)
                print(f'\n Fetching News articles for- {keyword} news\n')
        # keyword=request.GET.get('keyword')
        # print(keyword)
        # if not keyword:
        #     return Response("Keyword is required", status=status.HTTP_400_BAD_REQUEST)
        # Scrape tweets using the keyword
        # keyword=request.GET.get('keyword')
        # print (keyword)
                scraped_news = google_news_scraper(keyword) 
                #print (scraped_news)
        if scraped_news is None:
            return Response("Failed to scrape news", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Save the scraped tweets to the database in batches
        news_to_save = []
        for index,news_data in scraped_news.iterrows():
            #print(news_data.keys())
            news_obj = News(
                country=news_data['country'],
                source=news_data['source'],
                link=news_data['link'],
                title=news_data['title'],
                date=news_data['date'],
                description=news_data['description'],
                modified_dates=news_data['Modified Dates'],
                sentiment=news_data['sentiment']
               
            )
            news_to_save.append(news_obj)

        # Batch insert tweets into the database
        with transaction.atomic():
            News.objects.bulk_create(news_to_save)

        # Return response
        serializer = NewsSerializers(news_to_save, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)