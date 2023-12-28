import cv2
import mediapipe as mp
import numpy as np
import torch
from torch.utils.data import Dataset
import torch.nn as nn
import torch.nn.functional as F


class MyDataset(Dataset):
    def __init__(self, seq_list):
        self.X = []
        self.y = []
        for dic in seq_list:
            data = np.array(dic['value'])
            # 데이터 차원 변경: [depth, height, width] -> [1, depth, height, width]
            data = data.reshape(1, -1, 6, 6)

            self.y.append(dic['key'])
            self.X.append(data)

    def __getitem__(self, index):
        data = torch.tensor(self.X[index], dtype=torch.float32)
        label = torch.tensor(self.y[index], dtype=torch.long)
        return data, label

    def __len__(self):
        return len(self.X)

import torch.nn as nn
import torch.nn.functional as F




start_dot = 11
attention_dot = [n for n in range(start_dot, 29)]

# 라인 그리기
if start_dot == 11:
    """몸 부분만"""
    draw_line = [[11, 13], [13, 15], [15, 21], [15, 19], [15, 17], [17, 19], \
                [12, 14], [14, 16], [16, 22], [16, 20], [16, 18], [18, 20], \
                [23, 25], [25, 27], [24, 26], [26, 28], [11, 12], [11, 23], \
                [23, 24], [12, 24]]
    print('Pose : Only Body')

else:
    """얼굴 포함"""
    draw_line = [[11, 13], [13, 15], [15, 21], [15, 19], [15, 17], [17, 19], \
                [12, 14], [14, 16], [16, 22], [16, 20], [16, 18], [18, 20], \
                [23, 25], [25, 27], [24, 26], [26, 28], [11, 12], [11, 23], \
                [23, 24], [12, 24], [9, 10], [0, 5], [0, 2], [5, 8], [2, 7]]
    print('Pose : Face + Body')

def get_skeleton(video_path, pose_model):
    frame_length = 30
    xy_list_list = []
    cap = cv2.VideoCapture(video_path)

    if cap.isOpened():
        while True:
            ret, img = cap.read()
            if not ret:
                break
            img = cv2.resize(img, (640, 640))
            results = pose_model.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks:
                pose_data = [landmark.x for landmark in results.pose_landmarks.landmark] + \
                            [landmark.y for landmark in results.pose_landmarks.landmark]
                xy_list_list.append(pose_data)

    cap.release()

    # 프레임 길이에 맞게 데이터를 채우거나 줄임
    if len(xy_list_list) == 0:
        # xy_list_list가 비어있으면, 빈 리스트 반환
        return []
    elif len(xy_list_list) < frame_length:
        xy_list_list += [xy_list_list[-1]] * (frame_length - len(xy_list_list))
    elif len(xy_list_list) > frame_length:
        xy_list_list = xy_list_list[:frame_length]

    return xy_list_list


# Custom3DCNN 클래스 정의는 이전과 동일

class Custom3DCNN(nn.Module):
    def __init__(self, sequence_length, height, width):
        super(Custom3DCNN, self).__init__()
        self.conv1 = nn.Conv3d(in_channels=1, out_channels=16, kernel_size=(3, 3, 3), padding=1)
        self.conv2 = nn.Conv3d(16, 32, kernel_size=(3, 3, 3), padding=1)
        self.conv3 = nn.Conv3d(32, 64, kernel_size=(3, 3, 3), padding=1)
        self.pool = nn.MaxPool3d(kernel_size=(2, 2, 2), stride=2, padding=1)

        # 최종 feature map 크기 계산
        final_sequence_length = sequence_length // 8
        final_height = height // 8
        final_width = width // 8
        fc1_input_size = 64 * 5 * 2 * 2

        # 완전 연결 계층 정의
        self.fc1 = nn.Linear(fc1_input_size, 128)
        self.fc2 = nn.Linear(128, 2)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        # 여기서 x.size()를 출력하여 확인
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        # 여기서 x.size()를 출력하여 확인
        x = F.relu(self.conv3(x))
        x = self.pool(x)
        # 여기서 x.size()를 출력하여 확인
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

