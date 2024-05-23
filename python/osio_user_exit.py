#!/usr/bin/env python

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import time
import tomllib

display = Display(visible=0, size=(800, 600))
display.start()

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)

with open('./credit.toml', 'rb') as f:
    data = tomllib.load(f)
    username = data['osio']['username']
    password = data['osio']['password']
driver.get("https://osio-shop.peoplcat.com/login")
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="아이디를 입력해 주세요."]').send_keys(username)
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="비밀번호를 입력해 주세요."]').send_keys(password)
driver.find_element(By.CSS_SELECTOR, '.Button-sc-mznq07-0.LoginPage___StyledButton-sc-1ag2zbl-9.jVJpZh.hNBWCz').click()
time.sleep(1)

# 관리자 버튼
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/button[2]').click()
time.sleep(1)

# 설정 페이지 이동
driver.get("https://osio-shop.peoplcat.com/admin/settings")
time.sleep(1)

# 전체퇴장 보튼
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div[1]/div/div[1]/div[2]/button').click()
time.sleep(1)

# 확인 버튼
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, '.DialogButton-sc-9053cn-0.Confirm___StyledDialogButton2-sc-11bhi3f-4.inVSwg.kgkuiB').click()


driver.quit()
display.stop()






