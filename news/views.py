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
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response("start_date, and end_date are required.", status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parse start_date and end_date strings to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response("Invalid date format. Date format should be 'YYYY-MM-DD'.", status=status.HTTP_400_BAD_REQUEST)

        related_keywords = ["Autism spectrum disorder (asd)","Asperger's syndrome"]
        countries = ["Albania"]
                    #  ,"Afghanistan"]   
        news_to_save = []     
        for related_keyword in related_keywords:
            for country in countries:
                keyword = related_keyword+' '+ country
                print("keyword from view : ",keyword)
                print(f'\n Fetching News articles for- {keyword} news\n')
       
                scraped_news = google_news_scraper(keyword,start_date,end_date) 
                #print (scraped_news)
                if scraped_news is None:
                    return Response("Failed to scrape news", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
                # Save the scraped tweets to the database in batches
               
                for index,news_data in scraped_news.iterrows():
                    print("news data : ",news_data)
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
                    news_obj.save()
                    news_to_save.append(news_obj)
        
                # Batch insert tweets into the database
                # with transaction.atomic():
                #     News.objects.bulk_create(news_to_save)

        # Return response
        serializer = NewsSerializers(news_to_save, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)