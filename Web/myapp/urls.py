# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/', views.video_result, name='video_result'),
    path('upload_success/', views.upload_success, name='upload_success'),
    # 추가 URL 경로
]
