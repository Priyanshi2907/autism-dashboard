from django.db import models

class News(models.Model):
    country=models.CharField(max_length=100,blank=True, null=True)
    source=models.CharField(max_length=100,blank=True, null=True)
    link=models.URLField(blank=True, null=True)
    title=models.TextField(null=True,blank=True)
    modified_dates=models.CharField(max_length=100,null=True,blank=True)
    image=models.URLField(blank=True,null=True)
    # description=models.TextField(null=True,blank=True)
    # modified_dates=models.DateField(null=True,blank=True)
    # sentiment=models.CharField(max_length=100 , blank = True, null = True) 
    # def __str__(self):
    #     return f"{self.tweet_id} - {self.text[:50]}"  # Return a truncated version of the tweet text

    def to_json(self):
        return {
            "country": self.country,
            "source": self.source,
            "link": self.link,
            "title": self.title,  # Serialize datetime to ISO 8601 format
            "Date": self.modified_dates,
            "image": self.image
            # "description": self.description,
            # "modified_dates":self.modified_dates,
            # "sentiment": self.sentiment,
            
        }
