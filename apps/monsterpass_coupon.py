from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import time, json, requests
import pandas as pd

options = Options()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument("headless")
options.add_argument("--start-maximized")
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
def get_members(soup):
    members = soup.select('.ui-repeat.sc-cSHVUG.keecsQ > a > p > strong')
    phones = get_phones(members)
    return phones

# 전화번호 추출
def get_phones(members):
    phones = [m.text for m in members] 
    return phones

# 사용자별 정기권 추출하기
def get_tickets(phones):
    headers = {
        'token': '6e25d6162436a26d02eaf40b40d48654eb5f0212a59eb8aca7eecf9ed283558c',
    }
    tickets = []
    for p in phones:
        url = "https://api.monpass.im/api/crm/users/phone/" + p.replace('-','') + "/"
        res = requests.get(url, headers=headers)
        # print(res.status_code)
        res_data = res.json()
        tickets.append(res_data['data']['ticket'])
    return list(zip(phones, tickets))

# 티켓이 있는 사용자만 추출하기
def get_ticket_users(tickets):
    ticket_users = []
    for t in tickets:
        if t[1] != 0:
            ticket_users.append(t)
    return ticket_users

# 엑셀에 저장하기
def save_to_excel(data):
    now = datetime.now()
    col = ['phone', 'ticket']
    df = pd.DataFrame(data, columns=col)
    fname = f"{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}"
    df.to_excel(f'{fname}_ticket.xlsx', header=True, engine='openpyxl')


if __name__ == "__main__":
    url = "https://partner.monpass.im/"
    id = input('Your ID: ')
    passwd = input('Password: ')

    page_login(url, id, passwd)
    more_click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # 전체회원수 읽어오기
    t_member = soup.select_one('.sc-iFMziU.gNKmAv').text
    print("Total members: ", t_member[0:-1])

    # 명단에서 phone 번호만 추출하기
    phones = get_members(soup)
    print("Total phones: ", len(phones))

    # phone에 할당된 ticket 개수 가져오기(1시간, 2시간 구분 안됨)
    # (phone, ticket) 형식을 가진 리스트 
    tickets = get_tickets(phones)
    print("Total tickets: ", len(tickets))
    
    # ticket이 있는 사용자만 추출하기
    ticket_users = get_ticket_users(tickets)
    print("Total tickets: ", len(ticket_users))

    # 브라우저 닫기
    driver.quit()
    
    save_to_excel(tickets)
    save_to_excel(ticket_users)

    


   





