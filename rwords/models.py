from django.db import models

# Create your models here.
class rwords(models.Model):
    related_words=models.CharField(max_length=100,blank=True,null=True)

class tt(models.Model):
    trending_topic=models.CharField(max_length=100,blank=True,null=True)

class hashtags(models.Model):
    hashtags=models.CharField(max_length=100,blank=True,null=True)

# def to_json(self):
#         return {
#             "rwords": self.r,
#             "source": self.source,
#             "link": self.link,
#             "title": self.title,  # Serialize datetime to ISO 8601 format
#             "Date": self.modified_dates,
#             "image": self.image
#             # "description": self.description,
#             # "modified_dates":self.modified_dates,
#             # "sentiment": self.sentiment,
            
#         }

