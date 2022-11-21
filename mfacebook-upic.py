import time
import os
import wget
import re

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()

prefs = {'profile.default_content_setting_values.notifications': 2}

options.add_experimental_option('prefs', prefs)

profile_url = input('Enter the profile url (ex:https://m.facebook.com/arizaldinasti/) :')
album_url = input('Enter the folder url of current profile album (leave it empty to download pics of all folders) : ')
driver = webdriver.Chrome('F:/CODE/chromedriver_win32/chromedriver.exe', options=options)

driver.get('http://m.facebook.com')
time.sleep(5)

username = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="email"]')))
password = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="pass"]')))

# Login Fields
username.clear()
username.send_keys('Your Email or Phone number')
password.clear()
password.send_keys('Your Password')

login_btn = WebDriverWait(driver, 2).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="login"]'))).click()

time.sleep(5)

driver.get(profile_url)

time.sleep(5)

driver.get(profile_url + 'photos')

folders = []

if album_url :
    folders.append(album_url)
else :
    folders = driver.find_elements(By.CSS_SELECTOR, '.timeline.albums .item._50lb.tall.acw.abb a')
    folders = [f.get_attribute('href') for f in folders]

# Change scrolls value to higher to get more results
scrolls = 2
photos = []
for folder in folders:
    print(folder)

    driver.get(folder)
    time.sleep(4)

    for scr in range(1, scrolls):
        current_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script(f"window.scrollTo({current_height}, {scroll_height})")

        anchors = driver.find_elements(By.TAG_NAME, 'a')
        anchors = [a.get_attribute('href') for a in anchors]
        anchors = [a for a in anchors if str(a).startswith('https://m.facebook.com/photo')]

        for a in anchors:
            driver.get(a)
            time.sleep(4)
            pic = driver.find_element(By.CSS_SELECTOR, 'i[data-store*="imgsrc"]')
            pic = pic.get_attribute('data-store')[11:-2].replace('\\', '')
            photos.append(pic)

path = os.getcwd()

saved_folder = os.path.join(path, 'ScrappedPhotos')

# Create a directory
try :
    os.mkdir(saved_folder)
except :
    'The folder is already exist'

counter = 0
for photo in photos:
    save_as = os.path.join(saved_folder, str(counter) + '.jpg')
    wget.download(photo, save_as)
    counter += 1