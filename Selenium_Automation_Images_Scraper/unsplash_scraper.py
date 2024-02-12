# selenium 4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
import requests

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

URL = 'https://unsplash.com/'
driver.get(URL) # Goto Like of Website

# Scroll Down
height = 0
for i in range(20):
    height = height + 1000
    driver.execute_script("window.scrollTo(0, {});".format(height))
    if i < 10 :
        time.sleep(1)
    else:
        time.sleep(2)

# Get TAGs of Images
images_tags = driver.find_elements(By.XPATH, '//img[@class="tB6UZ a5VGX"]')

# Get URLs of Images
Images_urls = [img.get_attribute('src') for img in images_tags if 'images' in img.get_attribute('src')]

driver.close() # Close Firefox Window

while True:
    try:
        number = int(input("\nHow Many Images Do you want to Download from {} Photos?  ".format(len(Images_urls))))
        if number > len(Images_urls) or number <= 0:
            print("Please Enter a Number Between 1 : {}".format(len(Images_urls)))
        else:
            break
    except ValueError:
        print("Please Enter a Number")

# Download The Images
for index, url in enumerate(Images_urls[:number]):
    response = requests.get(url, stream=True)

    with open(f'Images/img-{index+1}.jpg', 'wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

