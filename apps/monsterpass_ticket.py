from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import time, json, requests
import pandas as pd
import os

def get_driver():
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("headless")
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver

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
            time.sleep(.2)
            print(".", end="")
        except:
            print("")
            break

# token 가져오기
def get_token():
    res_token = driver.execute_script("return localStorage.getItem('token')")
    print(f"token: {res_token}")
    return res_token

# member list 추출
def get_phones(soup):
    res_phone = soup.select('.ui-repeat.sc-cSHVUG.keecsQ > a > p > strong')
    phones = [p.text for p in res_phone]
    return phones
    
# 티켓이 있는 사용자만 티켓개수 추출하기
def get_ticket_user(tickets):
    ticket_user = []
    for t in tickets:
        if t[1] != 0:
            ticket_user.append(t)
    return ticket_user

def get_data(url, token):
    headers = {
        'token': token,
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    res_data = res.json()
    return res_data

# 사용자 ticket 정보 추출하기
def get_user_info(user, token):
    curl = "https://api.monpass.im/api/crm/users/phone/"
    ticket = []
    visit = []
    for phone in tqdm(user):
        # ticket 개수
        url = curl + phone.replace('-','') + "/"
        res_data = get_data(url, token)
        ticket.append(res_data['data']['ticket'])

        # 방문 시간
        # 전화번호만 등록되고 방문기록은 얺는 경우가 있음
        url = url + "logs?page=1"
        res_data = get_data(url, token)
        try:
            vtime = str(res_data['data']['rows'][0]['time'])[0:10]
        except:
            vtime = "0123456789"
            print(phone, ': Server is not responding.')
        visit.append(datetime.utcfromtimestamp(int(vtime)))

    return list(zip(phones, ticket, visit))

# ticket의 상세 개수 추출하기
def get_ticket_info(user, token):
    curl = "https://api.monpass.im/api/crm/users/phone/"
    data = []
    for phone, ticket, visit in user:
        url = curl + phone.replace('-','') + "/benefits/ticket"
        res_data = get_data(url, token)
        d1 = (phone, ticket, visit)
        for r in res_data['data']:
            d2 = d1 + (r['name'], r['count'], r['exp_date'])
            d1 = d2
        data.append(d2)
    return data

  
# 엑셀에 저장하기
def save_to_excel(data, col, prefix):
    t = datetime.now()
    df = pd.DataFrame(data, columns=col)
    df.index += 1
    fdate = t.strftime("%Y-%m-%d-%H-%M")
    df.to_excel(f"{fdate}_{prefix}.xlsx", header=True, engine='openpyxl')

def get_credit():
    try:
        with open('credit.txt', 'r') as file:
            credit = file.readlines()
            credit = [credit[0].strip(), credit[1].strip()]
    except:
        id = input('Your ID: ')
        passwd = input('Password: ')
        credit = ['id', 'passwd']
    return credit

if __name__ == "__main__":
 
    credit = get_credit()
    driver = get_driver()

    url = "https://partner.monpass.im/"
    page_login(url, credit[0], credit[1])
    token = get_token()

    more_click()
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    # 명단에서 phone 번호만 추출하기
    phones = get_phones(soup)

    # 중간확인
    total_user_cnt = soup.select_one('.sc-iFMziU.gNKmAv').text
    print(f"Total User Count: {total_user_cnt[0:-1]}")
    print(f"Number of phone: {len(phones)}")
    if int(total_user_cnt[0:-1]) != len(phones):
        print("User count and phone list count are dismatched")
        exit()

    # 전체 사용자에 대한 정보(ticket, visit)
    all_user_info = get_user_info(phones, token)

    # ticket 가진 사용자만 골라내기
    ticket_user = get_ticket_user(all_user_info)
    print(f"Ticket user count: {len(ticket_user)}")

    # ticket 가진 사용자의 종류별 티켓개수 추출하기
    ticket_info = get_ticket_info(ticket_user, token)
    
    # 브라우저 닫기
    driver.quit()

    #엑셀 저장
    col = None
    save_to_excel(ticket_info, col, f"ticket_{len(ticket_info)}")
    # col = ['Phone', 'Total ticket']
    save_to_excel(all_user_info, col, f"total_{len(all_user_info)}")

    
