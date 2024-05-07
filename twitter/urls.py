from django.urls import path
from . views import *

urlpatterns = [
    path('tweets/',PostTweets.as_view(),name="tweets"),
    #path('tweetsdate/',SearchTweets.as_view(),name="tweets"),
]
