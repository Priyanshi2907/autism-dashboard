from django.urls import path
from . views import *

urlpatterns = [
    path('tweets/',SearchTweets.as_view(),name="tweets"),
]
