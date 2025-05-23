from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
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
    notice = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[3]/button')
    if notice is True:
        notice.click()

    # login
    uname = driver.find_element(By.XPATH, '//*[@id="root"]/form/div[2]/div[1]/input')
    uname.send_keys(username)
    passwd = driver.find_element(By.XPATH, '//*[@id="root"]/form/div[2]/div[2]/input')
    passwd.send_keys(password)
    submit_button = driver.find_element(By.XPATH, '//*[@id="root"]/form/div[2]/button')
    submit_button.click()
    print("Login success" )
    # select admin or user
    admin_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/button[2]')
    admin_button.click()
    return

def quit_user(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/settings")
    quit_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[1]/div/div[1]/button')
    print(quit_button.text)
    quit_button.click()
    confirm_button = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div/footer/button[2]')
    confirm_button.click()
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
    csinfo_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[1]/button')
    csinfo_button.click()
    agree_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div/button')
    agree_button.click()
    download_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div/footer/button[2]')
    download_button.click()
    print("Starting download")
    time.sleep(10)
    return
