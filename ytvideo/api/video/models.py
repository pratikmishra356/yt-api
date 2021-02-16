from django.db import models
from django.utils.timezone import now
# Create your models here.

class Video(models.Model):
    video_id = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=1250)
    url = models.CharField(max_length=250,default='wY6UyatwVTA')
    upload_time = models.DateTimeField(default=now, blank=True)
    thumbnail = models.CharField(max_length=250)

