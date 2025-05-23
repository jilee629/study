from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import tomllib
import os
import time

def get_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {"download.default_directory": "/home/ubuntu/log"})
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

def enter_login(driver, username, password):
    driver.get("https://osio-shop.peoplcat.com/login")

    # notice window
    popup = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div')
    if popup is not None:
        ever_chk = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[3]/div').click()
        notice_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[3]/button').click()

    # login
    uname = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="아이디를 입력해 주세요."]').send_keys(username)
    passwd = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="비밀번호를 입력해 주세요."]').send_keys(password)
    submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    print("Login success" )
    # select admin or user
    manager_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/button[2]').click()
    return

def quit_user(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/settings")
    quit_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[1]/div/div[1]/button').click()
    confirm_btn = driver.find_element(By.XPATH, '//button[text()="확인"]').click()
    time.sleep(3)
    return

def get_count(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/entry")
    adult = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/header/div[2]/div/span[2]').text
    child = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/header/div[2]/div/span[4]').text
    print(f'-> Adult: {adult}, Child: {child}')
    return

def download_csinfo(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/users")
    csinfo_btn =  driver.find_element(By.XPATH, '//button[text()="고객 다운로드"]').click()
    agree_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div/button').click()
    download_btn = driver.find_element(By.XPATH, '//button[text()="다운로드"]').click()
    print("Starting download")
    time.sleep(10)
    return
