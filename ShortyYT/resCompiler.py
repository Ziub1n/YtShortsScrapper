import os

input_folder = "./DownloadedVideos/beforeEdit"
output_folder = "./DownloadedVideos/editedVideos"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):
    if file_name.endswith(".mp4"):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # Check if file size is 0 KB
        file_size = os.path.getsize(input_path)
        if file_size == 0:
            os.remove(input_path)
            print(f"Removed {file_name} because it has 0 KB size.")
        else:
            os.system(f'ffmpeg -i "{input_path}" -vf "scale=-1:1280:flags=lanczos" -c:v libx264 -crf 23 -preset veryfast -c:a copy "{output_path}"')
            print(f"{file_name} done")
