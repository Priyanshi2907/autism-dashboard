from rest_framework.response import Response
from django.shortcuts import render
from .scraper import *
from rest_framework.views import APIView
from . models import *
from .serializers import *
# Create your views here.

class Post_Related_Words(APIView):
    def get(self, request):
        
        # Call the function to fetch related words
        related_words_str = relatedwords_news()
        
        # Split the fetched string of related words into a list
        related_words_list = related_words_str.split(",")
    
        # Save each related word into the database row by row
        for word in related_words_list:
            word=word.strip()
            if not rwords.objects.filter(related_words__iexact=word).exists():
            # Create an instance of the model with the related word
                rwords_instance = rwords.objects.create(related_words=word)
        
                # Save the instance to the database
                rwords_instance.save()
    
        # Query all instances of the model and serialize the data
        queryset = rwords.objects.all()
        serializer = RSerializers(queryset, many=True)
        
        # Return the serialized data as an API response
        return Response(serializer.data)
    
class Get_Related_words(APIView):
    def get(self,request):
        # Query all instances of the model and serialize the data
        queryset = rwords.objects.all()
        serializer = RSerializers(queryset, many=True)
        
        # Return the serialized data as an API response
        return Response(serializer.data)
        

class Post_TT(APIView):
    def get(self, request):
        
        # Call the function to fetch related words
        tt_str = Trending_topics_news()
        
        # Split the fetched string of related words into a list
        tt_list = tt_str.split(",")
    
        # Save each related word into the database row by row
        for word in tt_list:
            word=word.strip()
            if not tt.objects.filter(trending_topic__iexact=word).exists():
            # Create an instance of the model with the related word
                tt_instance = tt.objects.create(trending_topic=word)
        
                # Save the instance to the database
                tt_instance.save()
        # Query all instances of the model and serialize the data
        queryset = tt.objects.all()
        serializer = TSerializers(queryset, many=True)
        
        # Return the serialized data as an API response
        return Response(serializer.data)
    
        
class Get_TT(APIView):
    def get(self,request):
        # Query all instances of the model and serialize the data
        queryset = tt.objects.all()
        serializer = TSerializers(queryset, many=True)
        
        # Return the serialized data as an API response
        return Response(serializer.data)
    


        
class Post_Hashtags(APIView):
    def get(self, request):
        
        # Call the function to fetch related words
        hashtags_str = Hashtags_twitter()
        
        # Split the fetched string of related words into a list
        hashtag_list = hashtags_str.split(",")
    
        # Save each related word into the database row by row
        for word in hashtag_list:
            word=word.strip()
            if not hashtags.objects.filter(hashtags__iexact=word).exists():
            # Create an instance of the model with the related word
                hash_instance = hashtags.objects.create(hashtags=word)
        
                # Save the instance to the database
                hash_instance.save()
        # Query all instances of the model and serialize the data
        queryset = hashtags.objects.all()
        serializer = HSerializers(queryset, many=True)
        
        # Return the serialized data as an API response
        return Response(serializer.data)
    
class Get_Hashtag(APIView):
    def get(self,request):
        # Query all instances of the model and serialize the data
        queryset = hashtags.objects.all()
        serializer = HSerializers(queryset, many=True)
        
        # Return the serialized data as an API response
        return Response(serializer.data)
        
