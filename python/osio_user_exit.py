#!/usr/bin/env python

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from datetime import datetime
import time
import tomllib
import os


now = datetime.now()
print(f'-> {now}')

display = Display(visible=0, size=(1024, 768))
display.start()

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)

credit = os.path.dirname(__file__) + '/credit.toml'
with open(credit, 'rb') as f:
    data = tomllib.load(f)
    username = data['osio']['username']
    password = data['osio']['password']

# login page
driver.get("https://osio-shop.peoplcat.com/login")
print(f'-> {driver.current_url}')
driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[1]/input').send_keys(username)
driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[2]/input').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="root"]/form/div/button').click()

# manager mode
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/button[2]').click()
print(f'-> {driver.current_url}')

# setting page
driver.get("https://osio-shop.peoplcat.com/admin/settings")
print(f'-> {driver.current_url}')
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/button').click()
driver.find_element(By.XPATH, '//*[@id="overlays"]/div/div/div/div[2]/div/button[2]').click()
time.sleep(3)

driver.quit()
display.stop()






