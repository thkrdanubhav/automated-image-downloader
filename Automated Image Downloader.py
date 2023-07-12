import time

import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import imghdr
import configparser
import datetime
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

def download_image(image_url, file_path, min_width=0, min_height=0, content_length=0):
    try:
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        ## content length check


        # Check if the image is a GIF
        if imghdr.what(None, h=image_response.content) == "gif":
            print("Skipping GIF image...")
            return False

        # Only download .jpeg, jpg and .png images

        with open(file_path, "wb") as file:
            file.write(image_response.content)
            print(f"Image downloaded: {file_path}")

        # Image size check
        if min_width > 0 and min_height > 0:
            img = Image.open(file_path)

            if not (img.width >= min_width and img.height >= min_height):
                os.remove(file_path)
                print("Skipping image: Dimensions are below the specified minimums")
                return False
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        raise Exception("Error threshold reached")

def download_images(keyword, num_images, max_error_count, timestamp, min_width=0, min_height=0, content_length=0):
    downloaded_count = 0
    page_num = 0

    while downloaded_count < num_images:
        start_index = page_num
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}&tbm=isch&start={start_index}"
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        image_links = list(set(soup.find_all("img")))

        for i, link in enumerate(image_links):
            error_count = 0
            if downloaded_count >= num_images:
                print(f"Downloaded count: {downloaded_count} is greater than num of images: {num_images}")
                break

            if error_count > max_error_count:
                print(f"Error count: {error_count} is greater than max error count: {max_error_count}")
                error_count = 0
                break

            image_url = link["src"]
            image_url = urllib.parse.urljoin("https://www.google.com/", image_url)
            print(f"Downloading images from link: {image_url}")
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            elif not image_url.startswith("http"):
                # If the scheme is missing, assume it's an HTTPS URL
                image_url = "https://" + image_url

            # Get image dimensions
            image_dimensions = link.get("data-w", None), link.get("data-h", None)
            if image_dimensions[0] is not None and image_dimensions[1] is not None:
                width = int(image_dimensions[0])
                height = int(image_dimensions[1])

                # Check if image dimensions are below the specified minimums
                print(f"Width of the image: {width}, height: {height}")
                if width < min_width or height < min_height:
                    print("Skipping image: Dimensions are below the specified minimums")
                    continue

            file_name = f"{keyword}_image_{downloaded_count + 1}.jpg"

            # Save the image to the specified directory
            file_path = os.path.join("images", str(timestamp), file_name)

            # Download the image
            time.sleep(0.1)
            if download_image(image_url, file_path, min_width, min_height, content_length):
                downloaded_count += 1
            else:
                print("Error Continue")
                error_count += 1
                continue
            error_count = 0
        time.sleep(0.5)
        page_num += 1

def download_images_threaded(keywords, num_images, min_width, min_height, max_error_count, content_length):
    timestamp = int(time.time())
    folder_path = os.path.join("images", str(timestamp))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    total_downloaded_count = 0
    total_error_count = 0
    timestamp = int(time.time())
    start_time = datetime.datetime.now()
    for keyword in keywords:
        keyword = keyword.lstrip('[').strip('"').rstrip('"')
        download_images(keyword, num_images, max_error_count, timestamp, min_width, min_height, content_length)

    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     for keyword in keywords:
    #         try:
    #             executor.submit(download_images, keyword, num_images, min_width, min_height)
    #             total_downloaded_count += num_images
    #
    #         except Exception as e:
    #             print(f"An error occurred for the keyword '{keyword}': {e}")
    #             total_error_count += 1

    end_time = datetime.datetime.now()
    total_time = end_time - start_time

    print("--- Summary ---")
    print(f"Current Date and Time: {end_time}")
    print(f"Total Images Downloaded: {total_downloaded_count}")
    print(f"Total Errors: {total_error_count}")
    print(f"Total Time Taken: {total_time}")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    keywords = config.get('Google Config', 'keywords').split(',')
    num_images = int(config.get('Google Config', 'num_images'))
    min_width = int(config.get('Google Config', 'min_width'))
    min_height = int(config.get('Google Config', 'min_height'))
    max_error_count = int(config.get("Google Config", 'max_error_count_per_keyword'))
    content_length = int(config.get('Google Config', 'content_length'))

    download_images_threaded(keywords, num_images, min_width, min_height, max_error_count, content_length)

