Automated Image Downloader

It downloads very large no. of images from web at once.

Working : 

  It was made using python and its libraries.
  The libraries used include :
  1 requests: To send HTTP requests and retrieve the web page content.
  2 BeautifulSoup: To parse and navigate through the HTML structure of the web page.
  3 urllib.parse: To handle URL encoding and joining.
  4 os: To create directories and manipulate file paths.
  5 imghdr: To determine the image file type.
  6 onfigparser: To read configuration settings from a file.
  7 datetime: To measure the execution time of the image downloading process.
  8 concurrent.futures.ThreadPoolExecutor: To parallelize the image downloading tasks.


* To run the code , run cofig.ini file and you can also make suitable changes in it according to your own needs.
* To download image according to your needs , just change the keywords !

Note : i have commented down the threads section of the code because it then downloads images very rapidly which leads to lot of restrictions i.e we will get blocked by 
sending too many requests.

Key Benefits : 
 1 Useful for machine learning data collection.
 2 Supports research and analysis with diverse image sets.
 3 Automates image downloading, saving time and effort.




 * I also made an genric version which downloads images from a particular url given by the user. (genric.py)
 * Another version which works with safari which uses selenium is also made i.e web_scraping_images.py (it downloads limited images)



For any improvements or work : thkrdanubhav@gmail.com
