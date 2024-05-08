from django.urls import path
from .views import *
urlpatterns = [
    path('news/',PostNews.as_view(),name="news"),


    #Current and last value
    path('current_last_value/',SentimentStatistics.as_view(),name="current_last_value"),
    # http://127.0.0.1:8000/current_last_value/

    #countrywisecount
    path('country_wise_count/',CountryWiseCount.as_view(),name="country_wise_count"),
    #http://127.0.0.1:8000/country_wise_count/?start_date=2024-04-06&end_date=2024-05-06&country=Albania


    #lineChart
    path('linechart/',LineChart.as_view(),name="linechart"),
   # http://127.0.0.1:8000/linechart/?country=Albania&sentiment=positive&start_date=2024-04-06&end_date=2024-05-06


    #Real time news 
    path('realtimenews/',realtimenews,name="real_time_news"),
    # sample eg:  /realtimenews/?sentiment=Positive&country=india&start_date=2024-03-06&end_date=2024-04-06

    

]
