from django.urls import path
from .views import *
urlpatterns = [
    path('post_rwords/',Post_Related_Words.as_view(),name="post_rwords"),
    path('get_rwords/',Get_Related_words.as_view(),name="get_rwords"),

    path('post_tt/',Post_TT.as_view(),name="post_tt"),
    path('get_tt/',Get_TT.as_view(),name="get_tt"),

    path('post_hash/',Post_Hashtags.as_view(),name="post_hash"),
    path('get_hash/',Get_Hashtag.as_view(),name="get_hash"),
    
    # path('getnews/',GetNews.as_view(),name="get_news"),
]