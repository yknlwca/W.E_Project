from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def make_clip_video(path, save_path, start_t, end_t):
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    clip_video = VideoFileClip(path).subclip(start_t, end_t)
    clip_video.write_videofile(save_path)

#파일 이름 변경 코드
import os
folder_path = '/content/drive/MyDrive/CCTV/Abnormal/Abnormal'
mp4_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]
mp4_files.sort()  # 파일을 정렬하여 이름을 순차적으로 변경합니다.
for i, file in enumerate(mp4_files, start=1):
    # 새 파일명 설정 (1.png, 2.png, ...)
    new_file_name = f"Abnormal_{i}.mp4"
#     # 파일 이름 변경
    os.rename(os.path.join(folder_path, file), os.path.join(folder_path, new_file_name))
print("파일 이름 변경 완료!")

path1 = '/content/drive/MyDrive/CCTV/Abnormal/Abnormal/C_3_12_1_BU_DYA_07-31_16-15-01_CA_RGB_DF2_M1.mp4'
path2 = '/content/drive/MyDrive/CCTV/Abnormal/Abnormal/C_3_12_25_BU_SYB_10-04_14-51-46_CB_RGB_DF2_F3.mp4'
path3 = '/content/drive/MyDrive/CCTV/Abnormal/Abnormal/C_3_12_25_BU_SYB_10-04_14-51-46_CC_RGB_DF2_F3.mp4'
path4 = '/content/drive/MyDrive/CCTV/Abnormal/Abnormal/C_3_12_25_BU_SYB_10-04_14-51-46_CD_RGB_DF2_F3.mp4'


# 초 단위
base_save_path = '/content/drive/MyDrive/CCTV/data/'
#1
make_clip_video(path1, os.path.join(base_save_path, 'b_081_abnormal_36.mp4'), 22, 34)
make_clip_video(path1, os.path.join(base_save_path, 'b_082_abnormal_30.mp4'), 41, 51)

make_clip_video(path1, os.path.join(base_save_path, 'b_081_normal_36.mp4'), 4, 16)
make_clip_video(path1, os.path.join(base_save_path, 'b_082_normal_30.mp4'), 11, 21)


#2
make_clip_video(path2, os.path.join(base_save_path, 'b_083_abnormal_36.mp4'), 22, 34)
make_clip_video(path2, os.path.join(base_save_path, 'b_084_abnormal_30.mp4'), 41, 51)

make_clip_video(path2, os.path.join(base_save_path, 'b_083_normal_36.mp4'), 4, 16)
make_clip_video(path2, os.path.join(base_save_path, 'b_084_normal_30.mp4'), 11, 21)


#3
make_clip_video(path3, os.path.join(base_save_path, 'b_085_abnormal_36.mp4'), 22, 34)
make_clip_video(path3, os.path.join(base_save_path, 'b_086_abnormal_30.mp4'), 41, 51)

make_clip_video(path3, os.path.join(base_save_path, 'b_085_normal_36.mp4'), 4, 16)
make_clip_video(path3, os.path.join(base_save_path, 'b_086_normal_30.mp4'), 11, 21)


#4
make_clip_video(path4, os.path.join(base_save_path, 'b_087_abnormal_36.mp4'), 22, 34)
make_clip_video(path4, os.path.join(base_save_path, 'b_088_abnormal_30.mp4'), 41, 51)

make_clip_video(path4, os.path.join(base_save_path, 'b_087_normal_36.mp4'), 4, 16)
make_clip_video(path4, os.path.join(base_save_path, 'b_088_normal_30.mp4'), 11, 21)

# 저장할 경로 정의
save_path = "/content/drive/MyDrive/CCTV/Data"
# 클립 소스 경로 정의
source_path = '/content/drive/MyDrive/CCTV/data'
if not os.path.exists(save_path):
    os.makedirs(save_path)
#1
abnormal1 = VideoFileClip(os.path.join(source_path, "b_081_abnormal_36.mp4"))
abnormal2 = VideoFileClip(os.path.join(source_path, "b_082_abnormal_30.mp4"))

normal1 = VideoFileClip(os.path.join(source_path, "b_081_normal_36.mp4"))
normal2 = VideoFileClip(os.path.join(source_path, "b_082_normal_30.mp4"))


combined_a = concatenate_videoclips([abnormal1, abnormal2])
combined_n = concatenate_videoclips([normal1, normal2])

combined_a.write_videofile(os.path.join(save_path, "bcom_019_abnormal_66.mp4"))
combined_n.write_videofile(os.path.join(save_path, "bcom_019_normal_66.mp4"))

#2
abnormal1 = VideoFileClip(os.path.join(source_path, "b_083_abnormal_36.mp4"))
abnormal2 = VideoFileClip(os.path.join(source_path, "b_084_abnormal_30.mp4"))

normal1 = VideoFileClip(os.path.join(source_path, "b_083_normal_36.mp4"))
normal2 = VideoFileClip(os.path.join(source_path, "b_084_normal_30.mp4"))


combined_a = concatenate_videoclips([abnormal1, abnormal2])
combined_n = concatenate_videoclips([normal1, normal2])

combined_a.write_videofile(os.path.join(save_path, "bcom_020_abnormal_66.mp4"))
combined_n.write_videofile(os.path.join(save_path, "bcom_020_normal_66.mp4"))

#3
abnormal1 = VideoFileClip(os.path.join(source_path, "b_085_abnormal_36.mp4"))
abnormal2 = VideoFileClip(os.path.join(source_path, "b_086_abnormal_30.mp4"))

normal1 = VideoFileClip(os.path.join(source_path, "b_085_normal_36.mp4"))
normal2 = VideoFileClip(os.path.join(source_path, "b_086_normal_30.mp4"))


combined_a = concatenate_videoclips([abnormal1, abnormal2])
combined_n = concatenate_videoclips([normal1, normal2])

combined_a.write_videofile(os.path.join(save_path, "bcom_021_abnormal_66.mp4"))
combined_n.write_videofile(os.path.join(save_path, "bcom_021_normal_66.mp4"))

#4
abnormal1 = VideoFileClip(os.path.join(source_path, "b_087_abnormal_36.mp4"))
abnormal2 = VideoFileClip(os.path.join(source_path, "b_088_abnormal_30.mp4"))

normal1 = VideoFileClip(os.path.join(source_path, "b_087_normal_36.mp4"))
normal2 = VideoFileClip(os.path.join(source_path, "b_088_normal_30.mp4"))


combined_a = concatenate_videoclips([abnormal1, abnormal2])
combined_n = concatenate_videoclips([normal1, normal2])

combined_a.write_videofile(os.path.join(save_path, "bcom_022_abnormal_66.mp4"))
combined_n.write_videofile(os.path.join(save_path, "bcom_022_normal_66.mp4"))

