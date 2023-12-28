# myapp/tasks.py

from celery import shared_task
from .views import process_and_save_video

@shared_task
def process_video_task(video_path):
    return process_and_save_video(video_path)
