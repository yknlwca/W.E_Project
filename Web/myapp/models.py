from django.db import models

# Create your models here.
# myapp/models.py
# myapp/models.py
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    processed_video_file = models.FileField(upload_to='processed_videos/', blank=True, null=True)
    alarm_time = models.DateTimeField(blank=True, null=True)
