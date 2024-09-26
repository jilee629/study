from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pandas as pd
import tomllib
from tqdm import tqdm
import time
import os

def get_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--start-maximized")
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


if __name__ == "__main__":

    driver = get_driver()
    username, password = get_credit()
    enter_login(username, password)
    cancel_account = os.path.dirname(__file__) + '/cancel_240926.xlsx'
    # cancel_account = os.path.dirname(__file__) + '/cancel_test.xlsx'
    df = pd.read_excel(cancel_account, dtype = 'str')
    phones = df['phone'].values.tolist()
    print(phones)

    for phone in phones:
        user_search = "https://osio-shop.peoplcat.com/admin/users/search"
        driver.get(user_search)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/div[2]/div[2]/input').send_keys(phone)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/div[2]/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/section/div[1]/div/div/button').click()
        visit = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/table/tr[1]/td').text
        ticket = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div[3]/div/table/tr/td').text
        ticket_str = "보유한 오시오 상품이 없습니다."
        
        if visit == "0회" and ticket == ticket_str:
            print(f'{phone} True {visit} {ticket}')
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[3]/button').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/div/div/div/div/div/div').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/footer/button[2]').click()
            time.sleep(1)
        else:
            print(f'{phone} False {visit} {ticket}')

