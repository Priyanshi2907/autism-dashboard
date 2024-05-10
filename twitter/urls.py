from django.urls import path
from . views import *

urlpatterns = [
    path('tweets/',PostTweets.as_view(),name="tweets"),

    #order by reach
    path('orderbyreach/',NameByReach.as_view(),name="news"),
    #url eg: /orderbyreach/?entity=Person&country=US&start_date=2024-01-01&end_date=2024-12-31

    #real time tweet
    path('realtimetweet/',RealTimeTweet.as_view(),name="real_time_tweet"),
    #url eg: http://127.0.0.1:8000/realtimetweet/?sentiment=PERSON&country=US&start_date=2024-01-01&end_date=2024-12-31

    #Hashtags pairs
    path('hashtagpairs/',hashtag_pairs,name="hashtag_pairs"),
    # sample eg:  http://127.0.0.1:8000/hashtagpairs/?country=india&start_date=2024-05-03&end_date=2024-05-04


    #path('tweetsdate/',SearchTweets.as_view(),name="tweets"),
]
