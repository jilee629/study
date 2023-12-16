from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import time
from tqdm import tqdm
import pandas as pd
import tomllib

def get_credit():
    try:
        with open('python/credit.toml', 'rb') as f:
            data = tomllib.load(f)
            username = data['monpass']['username']
            password = data['monpass']['password']
    except:
        username = input('Your ID: ')
        password = input('Password: ')
    return [username, password]

def get_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("headless")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def page_login(url, id, passwd):
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, '.ui-input-text input[name="id"]').send_keys(id)
    driver.find_element(By.CSS_SELECTOR, '.ui-input-text input[name="pw"]').send_keys(passwd)
    driver.find_element(By.CSS_SELECTOR, '.BU2.border.sc-bdVaJa.djlRTQ').click()
    time.sleep(1)
    return

def get_token():
    token = driver.execute_script("return localStorage.getItem('token')")
    print(f"Token: {token}")
    return token

def enter_memberpage():
    driver.get('https://partner.monpass.im/member')
    time.sleep(2)
    return

def more_click(total_user_cnt):
    for i in tqdm(range(50, int(total_user_cnt), 50), desc=' more_click'):
        driver.find_element(By.CSS_SELECTOR, '.sc-cBdUnI.fBYDFC').click()
        try:
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-cBdUnI.fBYDFC'))
            )
        except:
            break
    return

def get_total_user_cnt():
    total_user_cnt = driver.find_element(By.CSS_SELECTOR, '.sc-iFMziU.gNKmAv').text
    return int(total_user_cnt[0:-1])

def get_data(url, token):
    headers = {
        'token': token,
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    res_data = res.json()
    return res_data

# phone list 추출
def get_phone(soup):
    phone = soup.select('.ui-repeat.sc-cSHVUG.keecsQ > a > p > strong')
    phones = [p.text for p in phone]
    return phones

def get_ticket(phones, token):
    curl = "https://api.monpass.im/api/crm/users/phone/" 
    tickets = list()
    for phone in tqdm(phones, desc=' user_ticket'):
        url = curl + phone.replace('-','') + "/"
        res_data = get_data(url, token)
        ticket = res_data['data']['ticket']
        tickets.append(ticket)
    return tickets

def get_visit(phones, token):
    curl = "https://api.monpass.im/api/crm/users/phone/"
    visits = list()
    for phone in tqdm(phones, desc=' user_visit'):
        url = curl + phone.replace('-','') + "/" + "logs?page=1"
        res_data = get_data(url, token)
        try:
            vtime = str(res_data['data']['rows'][0]['time'])[0:10]
        except:
        # 전화번호만 등록되고 방문기록은 얺는 경우가 있음
            vtime = "0123456789"
            print(' ', phone, ': Server is not responding.')
        visit = datetime.utcfromtimestamp(int(vtime))
        visits.append(visit)
    return visits

# 티켓이 있는 사용자만 추출하기
def filter_ticketuser_phone(user_infos):
    ticketuser_phones = list()
    for info in tqdm(user_infos, desc=' ticket_user'):
        if info[1] != 0:
            ticketuser_phones.append(info[0])
    return ticketuser_phones

# ticket의 상세 개수 추출하기

def get_ticket_detail(phones, token):
    curl = "https://api.monpass.im/api/crm/users/phone/"
    ticket_info = list()
    for phone in tqdm(phones, desc=' ticket_info'):
        url = curl + phone.replace('-','') + "/benefits/ticket"
        res_data = get_data(url, token)
        data1 = list()
        for res in res_data['data']:
            data2 = data1 + [res['name'], res['count'], res['exp_date']]
            data1 = data2
        ticket_info.append(data1)
    return ticket_info

def data_align(phones, tickets, visits, detailtickets):
    data = list()
    for p, t, v, d in zip(phones, tickets, visits, detailtickets):
        data1 = [p, t, v]
        data1.extend(d)
        data.append(data1)
    return data

def save_to_excel(data, prefix):
    col = None
    t = datetime.now()
    df = pd.DataFrame(data, columns=col)
    df.index += 1
    fdate = t.strftime("%Y-%m-%d-%H-%M")
    df.to_excel(f"{fdate}_{prefix}.xlsx", header=True, engine='openpyxl')


if __name__ == "__main__":
 
    start = time.time()

    credit = get_credit()
    driver = get_driver()
    url = "https://partner.monpass.im/"

    page_login(url, credit[0], credit[1])
    token = get_token()
    enter_memberpage()

    # total_user_cnt = 500
    total_user_cnt = get_total_user_cnt()
    print(f"-> Total user count: {total_user_cnt}")
    more_click(total_user_cnt)

    # selenium보다 beautifulsoup이 속도가 더 빠름    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 전체 사용자에 대한 정보
    user_phones = get_phone(soup)
    print(f"-> Phone count: {len(user_phones)}")
    if total_user_cnt != len(user_phones):
        print('! Count dismatch')
        exit()

    user_ticket = get_ticket(user_phones, token)
    user_visit = get_visit(user_phones, token)
    total_ticket_cnt_1 = sum(user_ticket)
    print(f"-> Total ticket count 1: {total_ticket_cnt_1}")
    if total_user_cnt != len(user_ticket):
        print('! Count dismatch')
        exit()
    elif total_user_cnt != len(user_visit):
        print('! Count dismatch')
        exit()
    
    user_info = list(zip(user_phones, user_ticket, user_visit))
    save_to_excel(user_info, f"total_{len(user_phones)}_{total_ticket_cnt_1}")

    # ticket을 가진 사용자에 대한 상세 정보
    ticketuser_phones = filter_ticketuser_phone(user_info)
    print(f"-> Ticket users: {len(ticketuser_phones)}")
    ticketuser_ticket = get_ticket(ticketuser_phones, token)
    ticketuser_visit = get_visit(ticketuser_phones, token)
    ticketuser_ticket_info = get_ticket_detail(ticketuser_phones, token)
    total_ticket_cnt_2 = sum(ticketuser_ticket)
    print(f"-> Total ticket count 2: {total_ticket_cnt_2}\n")
    if len(ticketuser_phones) != len(ticketuser_ticket):
        print('! Count dismatch')
        exit()
    elif len(ticketuser_phones) != len(ticketuser_ticket_info):
        print('! Count dismatch')
        exit()

    ticketuser_info = data_align(ticketuser_phones, ticketuser_ticket,
                                  ticketuser_visit, ticketuser_ticket_info)
    save_to_excel(ticketuser_info, f"ticket_{len(ticketuser_phones)}_{total_ticket_cnt_2}")
    
    driver.quit()

    sec = time.time() - start
    print(f"Elapsed time : {timedelta(seconds=sec)}")
    
    

    
