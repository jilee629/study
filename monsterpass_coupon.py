from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())

id = input('Your ID: ')
password = input('Password: ')

driver = webdriver.Chrome(service=service, options=options)

# login
driver.get('https://partner.monpass.im/')
driver.find_element(By.NAME, 'id').send_keys(id)
driver.find_element(By.NAME, 'pw').send_keys(password)
driver.find_element(By.CSS_SELECTOR, '.BU2.border.sc-bdVaJa.djlRTQ').click()
time.sleep(1)

driver.get('https://partner.monpass.im/member')

element = driver.find_element(By.CSS_SELECTOR, '.sc-jzJRlG.ipeLkB')
element.send_keys(Keys.END)
# action = ActionChains(driver)
# action.move_to_element(element).perform()
