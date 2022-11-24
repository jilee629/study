from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
# 셀레니움 실행동안 브라우저 닫지 않기
options.add_experimental_option('detach', True)
# 개발도구 로그 보지 않기
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# 브라우저 화면 최대화
options.add_argument("--start-maximized")
# driver가 백그라운드에서 실행, 브라우져 화면 안보임 
options.add_argument("headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.google.com/')
data = driver.find_element(By.CSS_SELECTOR, '.MV3Tnb').text
print(f'결과 : {data}')
driver.quit()