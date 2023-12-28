import cv2
import mediapipe as mp
import torch
from torch.utils.data import DataLoader
import numpy as np
from .utils import MyDataset, Custom3DCNN, get_skeleton
from .models import Video
from django.core.files.storage import FileSystemStorage



sequence_length = 30
height = 6
width = 6

def process_and_save_video(video_path, model_path, device):
    # MediaPipe Pose 객체 초기화
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=1,
                        enable_segmentation=False, min_detection_confidence=0.5)

    # get_skeleton 함수를 사용하여 sequence_data 가져오기
    sequence_data = get_skeleton(video_path, pose)

    # sequence_data의 길이와 내용 확인
    print("sequence_data length:", len(sequence_data))
    if len(sequence_data) > 0:
        print("First element shape:", len(sequence_data[0]))

    # 시퀀스 데이터를 텐서로 변환
    sequence_tensor = torch.tensor(sequence_data, dtype=torch.float32).to(device)

    # 채널 차원 추가 후의 텐서 크기 확인
    sequence_tensor = sequence_tensor.unsqueeze(1)  # 채널 차원 추가
    print("sequence_tensor shape after unsqueeze:", sequence_tensor.shape)

    # 모델에 sequence_data를 입력
    with torch.no_grad():
        result = net(sequence_tensor)
        _, predicted = torch.max(result, 1)

    # 비디오 처리 로직
    cap = cv2.VideoCapture(video_path)
    img_list = []

    if cap.isOpened():
        while True:
            ret, img = cap.read()
            if ret:
                img = cv2.resize(img, (640, 640))
                img_list.append(img)
            else:
                break
    cap.release()

    # 3D CNN 모델 로딩
    model_path = 'C:/Users/user/Desktop/SeSaC/Final_Project/models/3DCNN_v500.pt'
    net = Custom3DCNN(sequence_length, height, width).to(device)
    checkpoint = torch.load(model_path, map_location=device)
    net.load_state_dict(checkpoint)
    net.eval()

    # 시퀀스 데이터를 텐서로 변환
    sequence_tensor = torch.tensor(sequence_data, dtype=torch.float32).to(device)
    sequence_tensor = sequence_tensor.unsqueeze(1)  # 채널 차원 추가
    print("sequence_tensor shape:", sequence_tensor.shape)

    # 모델에 sequence_data를 입력
    with torch.no_grad():
        result = net(sequence_tensor)
        _, predicted = torch.max(result, 1)
    print("Model output shape:", result.shape)
    print("Predicted:", predicted)

    # 결과에 따른 텍스트 및 시각적 표시
    status = 'Normal' if predicted.item() == 0 else 'Abnormal'
    text_color = (255, 0, 0) if predicted.item() == 0 else (0, 0, 255)

    for img in img_list:
        if status == 'Abnormal':
            cv2.putText(img, 'WARNING: Abnormal Activity Detected!', (50, img.shape[0] // 2), cv2.FONT_HERSHEY_COMPLEX,
                        1.0, text_color, 2)
            cv2.rectangle(img, (0, 0), (img.shape[1], img.shape[0]), text_color, 10)

        cv2.putText(img, status, (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1.0, text_color, 2)

    # 처리된 비디오 저장
    storage_location = 'C:/Users/user/Desktop/SeSaC/Final_Project/Web/storage'
    fs = FileSystemStorage(location=storage_location)
    output_video_name = 'processed_video.mp4'
    out = cv2.VideoWriter(fs.path(output_video_name), cv2.VideoWriter_fourcc(*'DIVX'), 30, (640, 640))
    for img in img_list:
        out.write(img)
    out.release()

    return fs.url(output_video_name), predicted.item()
