from django.urls import path
from .views import *
urlpatterns = [
    path('news/',PostNews.as_view(),name="news"),
    #path('newsdate/',SearchNews.as_view(),name="news")
]
