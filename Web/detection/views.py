from django.shortcuts import render, redirect
from .models import Video
from .forms import VideoForm
import cv2
import torch
import mediapipe as mp
from tqdm import tqdm
from .custom_cnn import Custom3DCNN, MyDataset

# 비디오 업로드를 처리하는 뷰
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_results', video_id=form.instance.id)
    else:
        form = VideoForm()
    return render(request, 'detection/upload_video.html', {'form': form})

# 비디오 분석 결과를 보여주는 뷰
def view_results(request, video_id):
    video = Video.objects.get(id=video_id)
    process_video(video.video_file.path)  # 비디오 분석을 위해 process_video 함수 호출
    return render(request, 'detection/view_results.html', {'video': video})

# 홈 페이지를 보여주는 뷰
def home(request):
    return render(request, 'detection/home.html')

# 비디오를 처리하고 이상 행동을 분석하는 함수
def process_video(video_path):
    sequence_length = 30
    height = 6
    width = 6
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = Custom3DCNN(sequence_length=30, height=6, width=6).to(device)
    model.load_state_dict(torch.load('C:/Users/user/Desktop/SeSaC/Final_Project/models/3DCNN_v500.pt'))
    model.eval()

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
    cv2.destroyAllWindows()

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.3)

    xy_list_list = []
    out_img_list = []
    for img in tqdm(img_list):
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            continue

        attention_dot = [n for n in range(11, 29)]
        draw_line_dic = {}
        for idx, x_and_y in enumerate(results.pose_landmarks.landmark):
            if idx in attention_dot:
                x, y = int(x_and_y.x * 640), int(x_and_y.y * 640)
                draw_line_dic[idx] = (x, y)

        xy_list = []
        for idx, x_and_y in enumerate(results.pose_landmarks.landmark):
            if idx >= 11:  # 어깨부터 발목까지
                xy_list.extend([x_and_y.x, x_and_y.y])
        draw_line = [[11, 13], [13, 15], [15, 21], [15, 19], [15, 17], [17, 19], \
                     [12, 14], [14, 16], [16, 22], [16, 20], [16, 18], [18, 20], \
                     [23, 25], [25, 27], [24, 26], [26, 28], [11, 12], [11, 23], \
                     [23, 24], [12, 24]]
        for line in draw_line:
            if line[0] in draw_line_dic and line[1] in draw_line_dic:
                img = cv2.line(img, draw_line_dic[line[0]], draw_line_dic[line[1]], (0, 255, 0), 4)

        xy_list_list.append(xy_list)
        if len(xy_list_list) == sequence_length:
            dataset = MyDataset([{'key': 0, 'value': xy_list_list}])
            data_loader = torch.utils.data.DataLoader(dataset)

            for data, _ in data_loader:
                data = data.to(device)
                with torch.no_grad():
                    result = model(data)
                    _, out = torch.max(result, 1)
                    status = 'Normal' if out.item() == 0 else 'Abnormal'
                    text_color = (255, 0, 0) if status == 'Normal' else (0, 0, 255)

                    cv2.putText(img, status, (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1.0, text_color, 2)

            xy_list_list = []

        out_img_list.append(img)

    filename = 'C:/Users/user/Desktop/SeSaC/Final_Project/cctv/results/3DCNN_result.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(filename, fourcc, 3, (640, 640), True)

    for out_img in out_img_list:
        out.write(out_img)

    out.release()
