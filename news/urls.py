from django.urls import path
from .views import *
urlpatterns = [
    path('news/',SearchNews.as_view(),name="news")
]
