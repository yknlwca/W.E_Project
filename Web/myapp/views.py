import cv2
import mediapipe as mp
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import VideoForm
from .models import Video
# myapp/views.py
from django.shortcuts import render

def index(request):
    # 여기에서 홈페이지를 렌더링하는 로직을 구현합니다.
    return render(request, 'myapp/index.html')


start_dot = 11
mp_pose = mp.solutions.pose
attention_dot = [n for n in range(start_dot, 29)]

# 라인 그리기
if start_dot == 11:
    """몸 부분만"""
    draw_line = [[11, 13], [13, 15], [15, 21], [15, 19], [15, 17], [17, 19], \
                [12, 14], [14, 16], [16, 22], [16, 20], [16, 18], [18, 20], \
                [23, 25], [25, 27], [24, 26], [26, 28], [11, 12], [11, 23], \
                [23, 24], [12, 24]]

else:
    """얼굴 포함"""
    draw_line = [[11, 13], [13, 15], [15, 21], [15, 19], [15, 17], [17, 19], \
                [12, 14], [14, 16], [16, 22], [16, 20], [16, 18], [18, 20], \
                [23, 25], [25, 27], [24, 26], [26, 28], [11, 12], [11, 23], \
                [23, 24], [12, 24], [9, 10], [0, 5], [0, 2], [5, 8], [2, 7]]



def process_and_save_video(video_path):
    cap = cv2.VideoCapture(video_path)
    img_list = []
    out_img_list = []

    if cap.isOpened():
        while True:
            ret, img = cap.read()
            if ret:
                img = cv2.resize(img, (640, 640))
                img_list.append(img)
            else:
                break

    cap.release()

    # MediaPipe 처리 로직
    pose = mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5)
    for img in img_list:
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            continue

        # 결과 프레임에 라인 그리기 등의 처리
        for line in draw_line:
            x1, y1 = int(results.pose_landmarks.landmark[line[0]].x * 640), int(results.pose_landmarks.landmark[line[0]].y * 640)
            x2, y2 = int(results.pose_landmarks.landmark[line[1]].x * 640), int(results.pose_landmarks.landmark[line[1]].y * 640)
            img = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 4)

        out_img_list.append(img)

    # 처리된 동영상 저장
    out = cv2.VideoWriter('/tmp/processed_video.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 30, (640, 640))
    for img in out_img_list:
        out.write(img)
    out.release()

    # 처리된 동영상의 URL 반환
    fs = FileSystemStorage(location='/tmp')
    output_video_url = fs.url('processed_video.mp4')
    return output_video_url

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            processed_video_url = process_and_save_video(video.video_file.path)
            return render(request, 'myapp/result.html', {'video_url': processed_video_url})
    else:
        form = VideoForm()
    return render(request, 'myapp/upload_video.html', {'form': form})

def example_view(request):
    # 다른 예시 페이지 로직
    return render(request, 'myapp/example.html')