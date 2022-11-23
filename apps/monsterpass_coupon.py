from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

options = Options()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

# login

# ID, Password 입력받기
id = input('Your ID: ')
password = input('Password: ')

# main page
driver.get('https://partner.monpass.im/')
driver.find_element(By.CSS_SELECTOR, '.ui-input-text input[name="id"]').send_keys(id)
driver.find_element(By.CSS_SELECTOR, '.ui-input-text input[name="pw"]').send_keys(passwd)
driver.find_element(By.CSS_SELECTOR, '.BU2.border.sc-bdVaJa.djlRTQ').click()
time.sleep(1)

# 회원관리 페이지
driver.get('https://partner.monpass.im/member')
time.sleep(1)

# 더보기 클릭해주기
while True:
    try:
        driver.find_element(By.CSS_SELECTOR, '.sc-cBdUnI.fBYDFC').click()
        time.sleep(.1)
    except:
        break

# member list 추출
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
members = soup.select('.ui-repeat.sc-cSHVUG.keecsQ > a > p > strong')

# 전화번호 추출
phones = [member.text for member in members] 

# 번호별 ticket 개수 추출
def get_ticket(phone):
    driver.find_element(By.NAME, 'search').send_keys(phone.replace('-',''))
    # 검색 클릭
    driver.find_element(By.CSS_SELECTOR, '.GY5.sc-kgoBCf.cxrvvx').click()
    time.sleep(.5)
    # 번호 클릭
    driver.find_element(By.CSS_SELECTOR, '.ui-repeat.sc-cSHVUG.keecsQ').click()
    time.sleep(.5)
    # ticket = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/article/aside/section/div[3]/button[2]/div/strong').text
    ticket = driver.find_element(By.CSS_SELECTOR, '.sc-bMVAic.greGXT button:nth-of-type(2) div strong').text
    driver.find_element(By.NAME, 'search').clear()
    return ticket

# 전화번호별 ticket 개수 검색
tickets = [get_ticket(phone) for phone in phones]

zip_list = zip(phones, tickets)
# [print(z) for z in zip_list]
print(len(list(zip_list)))

driver.quit()




