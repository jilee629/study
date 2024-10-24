#!/usr/bin/env python3

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

def get_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver

def get_credit():
    credit = os.path.dirname(__file__) + '/credit.toml'
    with open(credit, 'rb') as f:
        data = tomllib.load(f)
        username = data['osio']['username']
        password = data['osio']['password']
    return username, password

def enter_login(username, password):
    # login page
    url = "https://osio-shop.peoplcat.com/login"
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[1]/input').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[2]/input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/button').click()
    # manager mode
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/button[2]').click()
    return

def user_exit():
    # setting page
    url = "https://osio-shop.peoplcat.com/admin/settings"
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div[1]/div/div[1]/button').click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/footer/button[2]').click()
    time.sleep(3)
    return

def get_count():
    driver.get("https://osio-shop.peoplcat.com/admin/entry")
    adult = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/header/div[2]/div/span[2]').text
    child = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/header/div[2]/div/span[4]').text
    print(f'-> Adult: {adult}, Child: {child}')
    return


if __name__ == "__main__":

    display = Display(visible=0, size=(1024, 768))
    display.start()

    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S %A"))
    
    driver = get_driver()
    username, password = get_credit()
    enter_login(username, password)
    get_count()
    user_exit()
    get_count()

    driver.quit()
    display.stop()
















