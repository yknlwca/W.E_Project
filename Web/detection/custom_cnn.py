import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.utils.data import Dataset

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
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = F.relu(self.conv3(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class MyDataset(Dataset):
    def __init__(self, seq_list):
        self.X = []
        self.y = []
        for dic in seq_list:
            data = np.array(dic['value'])
            if data.size == 36:  # 36은 6*6, 모델이 기대하는 입력 크기와 일치해야 함
                data = data.reshape(1, -1, 6, 6)
                self.X.append(data)
                self.y.append(dic['key'])
            else:
                # 크기가 맞지 않을 때 적절한 조치를 취합니다.
                print(f"Incorrect data size: {data.size}, expected 36.")

    def __getitem__(self, index):
        data = torch.tensor(self.X[index], dtype=torch.float32)
        label = torch.tensor(self.y[index], dtype=torch.long)
        return data, label

    def __len__(self):
        return len(self.X)