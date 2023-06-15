from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
from bs4 import BeautifulSoup


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
        file_name = f'image_{counter}.jpg'  
        file_path = os.path.join('images', file_name)  # Specify the directory where you want to save the images
        with open(file_path, 'wb') as file:
            file.write(response.content)
        counter += 1  

        if counter >= 100:  # Break the loop once the minimum count is reached
            break


driver.quit()


