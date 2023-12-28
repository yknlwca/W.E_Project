# myapp/views.py

import cv2
import mediapipe as mp
import torch
from torch.utils.data import DataLoader
import numpy as np
from .models import Video
from .utils import MyDataset, Custom3DCNN
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .forms import VideoForm
from .video_processing import process_and_save_video


# 나머지 코드는 그대로 유지...


def index(request):
    # 홈페이지 렌더링
    return render(request, 'myapp/index.html')


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit = False)
            video.processed = True

            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            model_path = 'C:/Users/user/Desktop/SeSaC/Final_Project/3DCNN_v500.pt'  # 모델 파일 경로를 지정해주세요.
            processed_video_url, prediction = process_and_save_video(video.video_file.path, model_path, device)

            video.processed_video_file = processed_video_url  # 처리된 비디오의 URL을 저장
            video.save()  # 실제로 Video 객체를 데이터베이스에 저장

            return redirect('video_result', video_id=video.id, prediction=prediction)
        else:
            # 처리 실패 시 에러 메시지 처리
            return render(request, 'myapp/upload_video.html', {'form': form, 'error': '비디오 처리 중 오류 발생'})
    else:
        form = VideoForm()
        return render(request, 'myapp/upload_video.html', {'form': form})

def video_result(request, video_id):
    # 결과 페이지 뷰 로직
    video = Video.objects.get(id=video_id)
    return render(request, 'myapp/video_result.html', {'video': video})

def upload_success(request):
    # 업로드 성공 페이지
    return render(request, 'myapp/upload_success.html')
