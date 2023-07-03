import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import imghdr
import configparser
import datetime
from concurrent.futures import ThreadPoolExecutor

def download_image(image_url, file_path):
    try:
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        # Check if the image is a GIF
        #if imghdr.what(None, h=image_response.content) == "gif":
            #print("Skipping GIF image...")
            #return

        with open(file_path, "wb") as file:
            file.write(image_response.content)
            print(f"Image downloaded: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        raise Exception("Error threshold reached")

def download_images(keyword, num_images, min_width, min_height):
    downloaded_count = 0
    page_num = 0
    error_count = 0

    while downloaded_count < num_images:
        start_index = page_num * 100
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(keyword)}&tbm=isch&start={start_index}"
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        image_links = soup.find_all("img")

        for i, link in enumerate(image_links):
            if downloaded_count >= num_images:
                break

            image_url = link["src"]
            image_url = urllib.parse.urljoin("https://www.google.com/", image_url)

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
                if width < min_width or height < min_height:
                    print("Skipping image: Dimensions are below the specified minimums")
                    continue

            file_name = f"{keyword}_image_{downloaded_count + 1}.jpg"

            # Save the image to the specified directory
            file_path = os.path.join("images", file_name)

            # Download the image
            download_image(image_url, file_path)

            downloaded_count += 1
            error_count = 0

        page_num += 1

def download_images_threaded(keywords, num_images, min_width, min_height):
    if not os.path.exists("images"):
        os.makedirs("images")

    total_downloaded_count = 0
    total_error_count = 0

    start_time = datetime.datetime.now()

    with ThreadPoolExecutor(max_workers=4) as executor:
        for keyword in keywords:
            try:
                executor.submit(download_images, keyword, num_images, min_width, min_height)
                total_downloaded_count += num_images

            except Exception as e:
                print(f"An error occurred for the keyword '{keyword}': {e}")
                total_error_count += 1

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

    keywords = config.get('Config', 'keywords').split(',')
    num_images = int(config.get('Config', 'num_images'))
    min_width = int(config.get('Config', 'min_width'))
    min_height = int(config.get('Config', 'min_height'))

    download_images_threaded(keywords, num_images, min_width, min_height)
