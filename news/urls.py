from django.urls import path
from .views import *
urlpatterns = [
    path('news/',PostNews.as_view(),name="news"),

    path('getnews/',GetNews.as_view(),name="get_news"),


    #Current and last value
       #path('current_last_value/',SentimentStatistics.as_view(),name="current_last_value"),
    # http://127.0.0.1:8000/current_last_value/

    #countrywisecount
       #path('country_wise_count/',CountryWiseCount.as_view(),name="country_wise_count"),
    #http://127.0.0.1:8000/country_wise_count/?start_date=2024-04-06&end_date=2024-05-06&country=Albania


    #lineChart
       #path('linechart/',LineChart.as_view(),name="linechart"),
    # http://127.0.0.1:8000/linechart/?country=india&sentiment=Negative&start_date=2024-04-01&end_date=2024-04-30


    #Real time news 
       #path('realtimenews/',realtimenews,name="real_time_news"),
    # sample eg:  http://127.0.0.1:8000/realtimenews/?sentiment=Positive&country=india&start_date=2024-03-06&end_date=2024-04-06

    

]
