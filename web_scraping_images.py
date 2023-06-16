from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
from bs4 import BeautifulSoup


# User input for image details
num_images = int(input("Enter the number of images to download: "))
max_size = int(input("Enter the maximum size of the images (in bytes): "))
min_size = int(input("Enter the minimum size of the images (in bytes): "))

# Optional dimension input
dimensions_input = input("Enter the desired dimensions of the images (optional, leave blank to skip): ")
dimensions = dimensions_input.split("x") if dimensions_input else None

driver = webdriver.Safari()

# Open the desired URL
url = "https://in.images.search.yahoo.com/yhs/search;_ylt=Awrx.wqOrYlkK.4J5xjnHgx.;_ylu=Y29sbwMEcG9zAzEEdnRpZAMEc2VjA3BpdnM-?p=graph+images&type=ANYS3_D43OU_ext_bcr_%2460129_000000%24&param1=h4V77zECSIgvaawHmDS4wrdHZvefvDtppsLWeKoaeepgvQu3Xpuvrguamsd75aTsb4EW4UxLmp9T849VFgW_1Od8N9Ubml9ea01wxLDljvrdSdBYqMXi-dGMEvpNX7jc2_m8ripxPkuiBqbXQbanHr62YWjxSRXWz0qYsHHYBl4ct02fCkDofdsuSVbLGTMwX8msQQkJfSWppHSnJHmJ5D-8SyZ95QEV2xTeNpzQn5Ubm0G5TOZ2bFd-8HbpaGQG9YEHw5cRGe3xsFsdtyqkljbADAc2scHIwCTV_0xb5qEX-PS0fR0C44elNlmRwCmQ4jPtRpNS4YjwZZ5JLxd0GwTqbyjh1Xupd1XV7zNerWEPv26y&hsimp=yhs-SF01&hspart=Lkry&ei=UTF-8&fr=yhs-Lkry-SF01"
driver.get(url)
time.sleep(2)  # Add a delay to allow the page to load completely

html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')

images = soup.find_all('img')
counter = 0  # Counter variable to keep track of downloaded images
for i, img in enumerate(images):
    if 'src' in img.attrs:
        image_url = img['src']
        response = requests.get(image_url)

        # Check image size
        image_size = len(response.content)
        if image_size > max_size or image_size < min_size:
            continue

        # Check image dimensions
        if dimensions:
            image_dimensions = (int(img.get("width", 0)), int(img.get("height", 0)))
            if image_dimensions != tuple(dimensions):
                continue

        file_name = f'image_{counter}.jpg'
        file_path = os.path.join('images', file_name)  # Specify the directory where you want to save the images
        with open(file_path, 'wb') as file:
            file.write(response.content)

        counter += 1  
        if counter == num_images:
            break  

        if counter % 10 == 0:
            print(f"Downloaded {counter} images.")


