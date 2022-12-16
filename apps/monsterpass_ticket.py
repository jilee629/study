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
            print(".", end="")
        except:
            print("")
            break

# token 가져오기
def get_token():
    token = driver.execute_script("return localStorage.getItem('token')")
    print(f"token: {token}")
    return token

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
    for i, p in enumerate(phones):
        url = "https://api.monpass.im/api/crm/users/phone/" + p.replace('-','') + "/"
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res_data = res.json()
        tickets.append(res_data['data']['ticket'])
        if i%10 == 0:
            print(".", end="")
    print("")
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
        res.raise_for_status()
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
    fdate = f"{t.year}{t.month}{t.day}_{t.hour}_{t.minute}"
    df.to_excel(f"{fdate}_{prefix}.xlsx", header=True, engine='openpyxl')


if __name__ == "__main__":
    
    url = "https://partner.monpass.im/"
    id = input('Your ID: ')
    passwd = input('Password: ')

    page_login(url, id, passwd)
    token = get_token()
    more_click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # 전체회원수 읽어오기
    t_member = soup.select_one('.sc-iFMziU.gNKmAv').text
    print(f"Total members: {t_member[0:-1]}")

    # 명단에서 phone 번호만 추출하기
    phones = get_members(soup)
    print(f"Total phones: {len(phones)}")

    # 전체 사용자에 대해 ticket 조회하기
    total_users = get_tickets(phones, token)
    print(f"Verified users: {len(total_users)}")

    # ticket 가진 사용자만 전체 개수 추출하기
    ticket_users = get_user_tickets(total_users)
    print(f"Ticket users: {len(ticket_users)}")

    # ticket 가진 사용자만 시간별 개수 추출하기
    user_detail_tickets = get_detail_tickets(ticket_users, token)
    print(f"Detail user tickets: {len(user_detail_tickets)}")
    
    # 브라우저 닫기
    driver.quit()

    #엑셀 저장
    col = ['Phone', 'Total ticket']
    save_to_excel(total_users, col, f"total_{len(total_users)}")
    col = None
    save_to_excel(user_detail_tickets, col, f"detail_{len(user_detail_tickets)}")
    
