from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import datetime
import csv 
from django.urls import resolve
from django.test import RequestFactory 


class Command(BaseCommand):
    help = 'command to run url.py'
    
    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        print(now)

        # URL path to trigger
        url_path = '/post_tt/'

        # Resolve the URL pattern and get the view function
        resolver_match = resolve(url_path)
        view_func = resolver_match.func

        # Create a fake request object
        request_factory = RequestFactory()
        request = request_factory.get(url_path)

        # Call the view function
        response = view_func(request)

        # Print the response or perform further processing
        self.stdout.write(self.style.SUCCESS(str(response)))
        """
		Write Your Logic Here
	"""
	
print("Posting TT..........")