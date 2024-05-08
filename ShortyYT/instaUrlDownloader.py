import requests
import instaloader
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

loader = instaloader.Instaloader()

with open("./test2.txt", "r") as file:
    urls = [line.strip() for line in file]

for url in urls:
    time.sleep(2)
    try:

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')


        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        video_url = post.video_url

        filename = f"./DownloadedVideos/beforeEdit/{post.date_utc.strftime('%Y-%m-%d')}_{post.owner_username}_{post.shortcode}.mp4"

        with open(filename, "wb") as f:
            response = requests.get(video_url, stream=True)
            total_length = response.headers.get('content-length')
            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in tqdm(response.iter_content(chunk_size=4096), total=total_length, unit='B', unit_scale=True):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    print(f"\r[{filename}] Downloading... [{'=' * done}{' ' * (50-done)}] {dl/1024/1024:.2f}/{total_length/1024/1024:.2f} MB", end='', flush=True)

        print(f"\n{filename} downloaded.")

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")