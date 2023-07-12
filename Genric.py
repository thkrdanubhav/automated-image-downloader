import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_images(url, folder, num_images):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Set the headers to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <img> tags in the HTML
    image_tags = soup.find_all('img')

    # Variable to track the number of images downloaded
    num_images_downloaded = 0

    for image_tag in image_tags:
        # Break the loop if the desired number of images is downloaded
        if num_images_downloaded >= num_images:
            break

        # Check if the image tag has a 'src' attribute
        if 'src' not in image_tag.attrs:
            continue

        # Get the image URL
        image_url = image_tag['src']
        # Join the image URL with the base URL if it's a relative URL
        if not image_url.startswith('http'):
            image_url = urljoin(url, image_url)

        try:
            # Send a GET request to download the image with headers
            image_response = requests.get(image_url, headers=headers)
            image_response.raise_for_status()

            # Get the filename from the URL
            filename = os.path.basename(urlparse(image_url).path)

            # Save the image to the folder
            file_path = os.path.join(folder, filename)
            with open(file_path, 'wb') as file:
                file.write(image_response.content)

            print(f"Image downloaded: {file_path}")

            # Increment the count of downloaded images
            num_images_downloaded += 1
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")

    print(f"Total images downloaded: {num_images_downloaded}")

# Example usage
url = 'https://www.shutterstock.com/search/graph-x-y-axis'  # Replace with the desired URL
folder = 'images23'  # Replace with the desired folder name
num_images = 10  # Replace with the desired number of images to download

download_images(url, folder, num_images)
