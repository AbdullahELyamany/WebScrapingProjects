from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()

options.add_experimental_option('prefs', {
    # "download.default_directory": "/Users/hp/Downloads/data",
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

URL = "https://us.idec.com/idec-us/en/USD/Programmable-Logic-Controller/Micro-PLC/FT1A-SmartAXIS/p/FT1A-B12RC"

driver.get(URL)

driver.maximize_window()
driver.implicitly_wait(3)

cookie_div = driver.find_element(By.XPATH, '//div[@id="js-cookie-notification"]')
if cookie_div:
    driver.find_element(By.XPATH, '//div[@id="js-cookie-notification"]/button').click()

all_a_tags = driver.find_elements(By.XPATH, "//a")
count = 0

for a in all_a_tags:
    if a.get_attribute('href') and '.pdf' in a.get_attribute('href') and 'download' in a.text.lower():
        a.click()
        driver.implicitly_wait(3)
        time.sleep(10)

        count += 1
        if count >=5:
            break

time.sleep(15)
driver.close()
