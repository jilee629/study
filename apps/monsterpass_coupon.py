from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

options = Options()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("headless")
# options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

# 로그인 페이지에서 "회원관리" 페이지로 이동
def page_login(url, id, passwd):
    # login page
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, '.ui-input-text input[name="id"]').send_keys(id)
    driver.find_element(By.CSS_SELECTOR, '.ui-input-text input[name="pw"]').send_keys(passwd)
    driver.find_element(By.CSS_SELECTOR, '.BU2.border.sc-bdVaJa.djlRTQ').click()
    time.sleep(1)
    # 회원관리 페이지
    driver.get('https://partner.monpass.im/member')
    time.sleep(1)
    return

# 더보기 클릭 반복
def more_click():
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, '.sc-cBdUnI.fBYDFC').click()
            time.sleep(.1)
        except:
            break

# member list 추출
def get_members():
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    members = soup.select('.ui-repeat.sc-cSHVUG.keecsQ > a > p > strong')
    return members

# 전화번호 추출
def get_phones(members):
    phones = [member.text for member in members] 
    return phones

# 사용자별 정기권 가져오기
def get_user_ticket():
    user = 'https://api.monpass.im/api/crm/users/phone/01053253938/'
    headers = {
        'Authorization': 'access_token myToken'
        }
    reponse = requests.get(user, headers=headers)
    print(reponse)

# # user ticket 개수 추출 (4000개 이상에서 error 발생)
def get_tickets(phones):
    tickets = []
    for phone in phones:
        driver.find_element(By.NAME, 'search').send_keys(phone.replace('-',''))
        driver.find_element(By.CSS_SELECTOR, '.GY5.sc-kgoBCf.cxrvvx').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '.ui-repeat.sc-cSHVUG.keecsQ').click()
        time.sleep(2)
        ticket = driver.find_element(By.CSS_SELECTOR, '.sc-bMVAic.greGXT button:nth-of-type(2) div strong').text
        driver.find_element(By.NAME, 'search').clear()
        tickets.append(ticket)
    return tickets

# 엑셀에 저장하기
def save_to_excel(phones, tickets):
    data = list(zip(phones, tickets))
    print(len(data))
    col = ['phone', 'ticket']
    data_frame = pd.DataFrame(data, columns=col)
    data_frame.to_excel('ticket.xlsx', startrow=1, header=True, engine='openpyxl')


if __name__ == "__main__":
    url = 'https://partner.monpass.im/'
    id = input('Your ID: ')
    passwd = input('Password: ')

    page_login(url, id, passwd)
    # more_click()

    members = get_members()
    phones = get_phones(members)
    print(phones)
    print(f'phones : {len(phones)}')

    tickets = get_tickets(phones)

    driver.quit()





