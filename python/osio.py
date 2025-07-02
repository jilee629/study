from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import tomllib
import os
import time

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    if os.name != 'nt':
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {"download.default_directory": "/home/ubuntu/study/log"})
        service = Service(ChromeDriverManager().install())
    else:
        service = Service()
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
        # checkbox
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[3]/div').click()
        driver.find_element(By.XPATH, '//button[text()="닫기"]').click()

    # login
    driver.find_element(By.XPATH, '//*[@placeholder="아이디를 입력해 주세요."]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@placeholder="비밀번호를 입력해 주세요."]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@type="submit"]').click()
    print("Login success" )
    # select manager
    driver.find_element(By.XPATH, '//button[contains(., "manager")]').click()
    return

def quit_user(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/settings")
    driver.find_element(By.XPATH, '//button[contains(., "고객 전체 퇴장")]').click()
    driver.find_element(By.XPATH, '//button[text()="확인"]').click()
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
    driver.find_element(By.XPATH, '//button[text()="고객 다운로드"]').click()
    driver.find_element(By.XPATH, '//button[contains(., "위 내용에 동의합니다")]').click()
    driver.find_element(By.XPATH, '//button[text()="다운로드"]').click()
    print("Starting download")
    time.sleep(10)
    return
