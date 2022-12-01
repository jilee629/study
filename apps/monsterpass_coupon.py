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
def get_tickets(phones, token):
    headers = {
        'token': token,
    }
    tickets = []
    for p in phones:
        url = "https://api.monpass.im/api/crm/users/phone/" + p.replace('-','') + "/"
        res = requests.get(url, headers=headers)
        res_data = res.json()
        tickets.append(res_data['data']['ticket'])
    return list(zip(phones, tickets))

# 티켓이 있는 사용자만 추출하기
def get_user_tickets(tickets):
    user_tickets = []
    for t in tickets:
        if t[1] != 0:
            user_tickets.append(t)
    return user_tickets

# ticket의 상세 개수 추출하기
def get_detail_tickets(user_tickets, token):
    headers = {
        'token': token,
    }
    user_detail_tickets = []
    for p, t in user_tickets:
        url = "https://api.monpass.im/api/crm/users/phone/" + p.replace('-','') + "/benefits/ticket"
        res = requests.get(url, headers=headers)
        res_data = res.json()
        d1 = (p, t)
        for r in res_data['data']:
            d2 = d1 + (r['name'], r['count'])
            d1 = d2
        user_detail_tickets.append(d2)
    return user_detail_tickets
   
# 엑셀에 저장하기
def save_to_excel(data, col, prefix):
    t = datetime.now()
    df = pd.DataFrame(data, columns=col)
    df.index += 1
    fname = f"{t.year}{t.month}{t.day}_{t.hour}{t.minute}{t.second}"
    df.to_excel(f'{prefix}_{fname}.xlsx', header=True, engine='openpyxl')


if __name__ == "__main__":
    
    url = "https://partner.monpass.im/"
    id = input('Your ID: ')
    passwd = input('Password: ')

    # token을 추출하는 방법이 필요함. 현재는 직접 입력
    token = '9f8ef675397e6f48ebc07a9cd1936c1581f0786735ad450a4f8837f678f4aa70'

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

    # phone에 할당된 ticket 전체 개수 가져오기
    tickets = get_tickets(phones, token)
    print("Total tickets: ", len(tickets))

    # ticket 가진 사용자만 ticket 전체 개수 추출하기
    user_tickets = get_user_tickets(tickets)
    print("User ticket: ", len(user_tickets))
    
    # ticket 가진 사용자만 시간별 개수 추출하기
    user_detail_tickets = get_detail_tickets(user_tickets, token)
    print("User detail tickets: ", len(user_detail_tickets))
    
    # 브라우저 닫기
    driver.quit()


    #엑셀 저장
    col = ['Phone', 'Total ticket']

    # Total tickets
    # save_to_excel(tickets, col, f"total_{len(tickets)}")

    # User tickets
    # save_to_excel(user_tickets, col, f"user_{len(user_tickets)}") 

    # # User detail tickets
    col = None
    save_to_excel(user_detail_tickets, col, f"detail_{len(user_detail_tickets)}")
