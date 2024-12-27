import os
import requests
import time
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from joblib import Parallel,delayed

def sanitize_filename(file_name):
    return file_name.replace('/', '_').replace(':', '_')

# Function to set up the Chrome driver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-minimized")

    # Detect the operating system and set the path accordingly
    if platform.system() == "Windows":
        service = Service(executable_path="driver/chromedriver.exe")
    else:
        service = Service(executable_path="driver/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

# Function to download the video
def download_video(url, filename):
    # Ensure the 'videos' directory exists
    if not os.path.exists('videos'):
        os.makedirs('videos')

    # Construct the full file path
    file_path = os.path.join('videos', filename)

    print(f"Saving to: {file_path}")  # Debugging the file path

    try:
        print(f"Downloading: {filename}")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Download complete: {file_path}")
        else:
            print(f"Failed to download: {url} (Status code: {response.status_code})")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Function to get the download link from the webpage
def get_download_link(vidoza_url):
    driver = setup_driver()
    driver.get(vidoza_url)
    wait = WebDriverWait(driver, 10)
    
    # Wait for the video player to load
    video_player = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
    
    # Extract file name and video URL
    try:
       h2_elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/h1")
       h2_file = h2_elem.text.strip()
       file_name = f"{h2_file}.mp4"
       
      # Ensure correct attribute
    except Exception as e:
        print(f"could not find file name from H1 tag:{e}")
        file_name = "default_video.mp4"

    file_name = sanitize_filename(file_name)  # Sanitize the filename
    video_url = video_player.get_attribute('src')
    
    print(f"File Name Found: {file_name}")
    print(f"Download Link Found: {video_url}")
    
    return file_name, video_url

# Function to read links from the input file
def read_links_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    else:
        print(f"{file_path} does not exist.")
        return []

# Main function to drive the process
def main():
    driver = setup_driver()

    # Read video links from the links.txt file
    links = read_links_from_file('links.txt')
    
    for i, link in enumerate(links, 1):
        print(f"Processing {i}/{len(links)}: {link}")
        file_name, video_url = get_download_link(driver, link)
        if video_url:
            download_video(video_url, file_name)
    
    driver.quit()
if __name__ == "__main__":
    links = read_links_from_file('links.txt')
    Parallel(n_jobs=2)(delayed(get_download_link)(link) for link in links)
    main()
    
    
    
