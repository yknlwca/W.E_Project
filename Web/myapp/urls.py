from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('example/', views.example_view, name='example'),
    # 추가 URL 경로
]
