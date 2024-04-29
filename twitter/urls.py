from django.urls import path
from . views import *

urlpatterns = [
    path('tweets/<str:keyword>/',SearchTweets.as_view(),name="tweets"),
]
