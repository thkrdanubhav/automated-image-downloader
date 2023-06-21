#Image downloader , download as many images as you want and change the keyord & no. of images according to your needs !
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

def download_images(keyword, num_images):
    
    if not os.path.exists(keyword):
        os.makedirs(keyword)

    # Track the number of downloaded images
    downloaded_count = 0

   
    page_num = 0

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

          
            if image_url.startswith("//"):
                image_url = "https:" + image_url

           
            try:
                image_response = requests.get(image_url)
                image_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image: {e}")
                continue

           
            file_name = f"{keyword}_image_{downloaded_count + 1}.jpg"

            # Save the image to the specified directory
            file_path = os.path.join(keyword, file_name)
            with open(file_path, "wb") as file:
                file.write(image_response.content)
                print(f"Image downloaded: {file_path}")

            downloaded_count += 1

        page_num += 1


keyword = "graph images"
num_images = 1000
download_images(keyword, num_images)






# Made by Anubhav & Yash !
