from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import time

options = Options()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")

id = input('Your ID: ')
password = input('Password: ')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# login
driver.get('https://partner.monpass.im/')
driver.find_element(By.NAME, 'id').send_keys(id)
driver.find_element(By.NAME, 'pw').send_keys(password)
driver.find_element(By.CSS_SELECTOR, '.BU2.border.sc-bdVaJa.djlRTQ').click()
time.sleep(1)

# membership
driver.get('https://partner.monpass.im/member')
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
print(soup.text)

# driver.close()
