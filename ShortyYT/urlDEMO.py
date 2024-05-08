from undetected_chromedriver import Chrome, ChromeOptions
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import time

# Profiles to search for videos
profiles = ["the_goodfilms"]

max_posts = 400

chrome_options = ChromeOptions()
chrome_options.add_argument('--user-data-dir=./Application Support/Google/Chrome/')
chrome_options.add_argument('--profile-directory=Profile 6')
chrome_options.add_argument('--disable-extensions')
#chrome_options.add_argument('--headless')

browser = uc.Chrome(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    options=chrome_options)

def has_multiple_media_elements(element):
    try:
        element.find_element(By.CSS_SELECTOR, ".coreSpriteSidecarIconLarge")
        return True
    except NoSuchElementException:
        return False

def load_more_posts():
    last_height = browser.execute_script("return document.body.scrollHeight")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = browser.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        return False
    return True

try:
    for profile in profiles:
        print(f"Searching for videos on {profile}'s profile...")

        browser.get(f"https://www.instagram.com/{profile}/")
        time.sleep(5)

        video_links = set()

        while len(video_links) < max_posts:
            load_more_posts()
            time.sleep(2)

            elements = browser.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')
            for element in elements:
                if has_multiple_media_elements(element):
                    continue

                link = element.get_attribute('href')
                video_links.add(link)

                if len(video_links) >= max_posts:
                    break

        for link in video_links:
            browser.get(link)
            time.sleep(2)
            try:
                browser.find_element(By.CSS_SELECTOR, 'video')

                with open("./videosURL/test.txt", "a") as f:
                    f.write(link + "\n")
                    print(f"Post link saved: {link}")
            except NoSuchElementException:
                print(f"No video found for post: {link}")

finally:
    browser.quit()

