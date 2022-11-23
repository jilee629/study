from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# ID, Password 입력받기
id = input('Your ID: ')
passwd = input('Password: ')

options = Options()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

# login
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
print(f'phones : {len(phones)}')

# # 번호별 ticket 개수 추출
# # 함수 사용할 때 리스트가 많으면 에러 발생
def get_ticket(phone):
    driver.find_element(By.NAME, 'search').send_keys(phone.replace('-',''))
    driver.find_element(By.CSS_SELECTOR, '.GY5.sc-kgoBCf.cxrvvx').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '.ui-repeat.sc-cSHVUG.keecsQ').click()
    time.sleep(2)
    # ticket = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/article/aside/section/div[3]/button[2]/div/strong').text
    ticket = driver.find_element(By.CSS_SELECTOR, '.sc-bMVAic.greGXT button:nth-of-type(2) div strong').text
    driver.find_element(By.NAME, 'search').clear()
    print(phone, ticket)
    return ticket

tickets = [get_ticket(phone) for phone in phones]
print(f'tickes : {len(tickets)}')

# # 함수 사용하지 않는걸로 시험결과 -> 동일
# tickets = []
# for phone in phones:
#     driver.find_element(By.NAME, 'search').send_keys(phone.replace('-',''))
#     driver.find_element(By.CSS_SELECTOR, '.GY5.sc-kgoBCf.cxrvvx').click()
#     time.sleep(1)
#     driver.find_element(By.CSS_SELECTOR, '.ui-repeat.sc-cSHVUG.keecsQ').click()
#     time.sleep(1)
#     ticket = driver.find_element(By.CSS_SELECTOR, '.sc-bMVAic.greGXT button:nth-of-type(2) div strong').text
#     driver.find_element(By.NAME, 'search').clear()
#     tickets.append(ticket)

driver.quit()

data = list(zip(phones, tickets))
print(len(data))
col = ['phone', 'ticket']
data_frame = pd.DataFrame(data, columns=col)
data_frame.to_excel('ticket.xlsx', startrow=1, header=True, engine='openpyxl')



