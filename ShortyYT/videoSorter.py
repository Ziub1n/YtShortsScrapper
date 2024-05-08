import os
import random
import shutil
from moviepy.editor import VideoFileClip

def get_video_duration(video_path):
    try:
        with VideoFileClip(video_path) as clip:
            duration = clip.duration
        return duration
    except Exception as e:
        print(f"Error getting duration of {video_path}: {e}")
        return 0

def move_videos_to_folders(input_folder):
    if not os.path.exists(input_folder):
        print("Folder nie istnieje.")
        return

    video_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]

    if not video_files:
        print("Brak plików wideo w folderze.")
        return

    random.shuffle(video_files)

    folder_index = 1
    current_duration = 0
    num_videos_in_folder = 0

    for video_file in video_files:
        video_path = os.path.join(input_folder, video_file)
        video_duration = get_video_duration(video_path)

        if num_videos_in_folder == 0 or current_duration + video_duration > 780:
            folder_index += 1
            current_duration = 0
            num_videos_in_folder = 0

        target_folder = os.path.join(input_folder, f"folder_{folder_index}")
        os.makedirs(target_folder, exist_ok=True)

        target_path = os.path.join(target_folder, video_file)
        try:
            shutil.move(video_path, target_path)
            current_duration += video_duration
            num_videos_in_folder += 1
            print(f"{video_file} przeniesiony do {target_folder}")
        except Exception as e:
            print(f"Error moving {video_file}: {e}")

input_folder = "./DownloadedVideos/editedVideos"
move_videos_to_folders(input_folder)
