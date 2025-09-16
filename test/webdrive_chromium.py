from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from pyvirtualdisplay import Display
import tomllib
import os
import time

def get_driver():
    # service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {"download.default_directory": "/home/ubuntu/log"})
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def get_credit():
    credit = os.path.dirname(__file__) + '../python/credit.toml'
    with open(credit, 'rb') as f:
        data = tomllib.load(f)
        username = data['osio']['username']
        password = data['osio']['password']
    return username, password

def enter_login(username, password):
    # login page
    url = "https://osio-shop.peoplcat.com/login"
    driver.get(url)
    print("login :", driver.current_url)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[1]/input').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[2]/input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/button').click()
    print("select:", driver.current_url)
    # manager mode
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/button[2]').click()
    print("entry :", driver.current_url)
    return

def download_csinfo():
    driver.get("https://osio-shop.peoplcat.com/admin/users")
    print("user  :", driver.current_url)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[1]/button').click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div/footer/button[2]').click()
    print("Starting download")
    time.sleep(10)
    return

if __name__ == "__main__":

    display = Display(visible=0, size=(1024, 768))
    display.start()

    driver = get_driver()
    username, password = get_credit()
    enter_login(username, password)
    download_csinfo()
    print('OK')

    driver.quit()
    display.stop()