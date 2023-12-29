from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    processed = models.BooleanField(default=False)

    class Meta:
        app_label = 'detection'
    # 추가 필드 필요시 여기에 추가
