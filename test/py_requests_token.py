from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import time, json, requests
import pandas as pd

options = Options()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("headless")
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

id = input('Your ID: ')
passwd = input('Password: ')
url = "https://partner.monpass.im/"
driver.get(url)
driver.find_element(By.CSS_SELECTOR, '.ui-input-text input[name="id"]').send_keys(id)
driver.find_element(By.CSS_SELECTOR, '.ui-input-text input[name="pw"]').send_keys(passwd)
driver.find_element(By.CSS_SELECTOR, '.BU2.border.sc-bdVaJa.djlRTQ').click()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
# url = "https://api.monpass.im/api/crm/shop/introimg/"
url = "https://socket.monpass.im:7777/socket.io/?EIO=3&transport=polling&t=OJCsr64&sid=j-CmYJKxv-gTclOOFiJw"

res = requests.get(url, headers=headers)
print(res.status_code)
print(res.text)
