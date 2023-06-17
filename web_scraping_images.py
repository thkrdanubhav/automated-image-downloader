#web scrapper : download graph images or any image of your choice !

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
from bs4 import BeautifulSoup
import random


# User input for image details
num_images = int(input("Enter the number of images to download: "))
max_size = int(input("Enter the maximum size of the images (in bytes): "))
min_size = int(input("Enter the minimum size of the images (in bytes): "))

# Optional dimension input
dimensions_input = input("Enter the desired dimensions of the images (optional, leave blank to skip): ")
dimensions = dimensions_input.split("x") if dimensions_input else None

# User input for image source (random or URL)
image_source = input("Choose the image source (random/url): ")

if image_source.lower() == "random":
    random_url = "https://www.istockphoto.com/photos/x-y-graph"  # url which provides random graph images
else:
    url = input("Enter the URL to scrape images from: ")
    random_url = None

driver = webdriver.Safari()

# Open the desired URL or random URL
if random_url:
    driver.get(random_url)
else:
    driver.get(url)
    
time.sleep(2)  # Add a delay to allow the page to load completely

html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')

images = soup.find_all('img')
counter = 0  
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

driver.quit()












# url : https://www.shutterstock.com/search/graph-x-y-axis
# Made by Anubhav & Yash 


    


