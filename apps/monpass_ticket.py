from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import time
from tqdm import tqdm
import pandas as pd

def get_credit():
    try:
        with open('credit', 'r') as file:
            credit = file.readlines()
            credit = [credit[0].strip(), credit[1].strip()]
    except:
        id = input('Your ID: ')
        passwd = input('Password: ')
        credit = ['id', 'passwd']
    return credit

def get_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("headless")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
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
    return token

def enter_memberpage():
    driver.get('https://partner.monpass.im/member')
    time.sleep(2)
    return

def more_click(total_user_cnt):
    for i in tqdm(range(50, int(total_user_cnt), 50), desc='more_click'):
        driver.find_element(By.CSS_SELECTOR, '.sc-cBdUnI.fBYDFC').click()
    time.sleep(2)
    return

def get_total_user_cnt():
    total_user_cnt = driver.find_element(By.CSS_SELECTOR, '.sc-iFMziU.gNKmAv').text
    return total_user_cnt[0:-1]

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
    '''
    ['010-4213-7811', '010-4031-7134',]
    '''

def get_ticket(phones, token):
    curl = "https://api.monpass.im/api/crm/users/phone/" 
    tickets = list()
    for phone in tqdm(phones, desc='user_ticket'):
        url = curl + phone.replace('-','') + "/"
        res_data = get_data(url, token)
        ticket = res_data['data']['ticket']
        tickets.append(ticket)
    # print(tickets)
    return tickets
    '''
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    '''

def get_visit(phones, token):
    curl = "https://api.monpass.im/api/crm/users/phone/"
    visits = list()
    for phone in tqdm(phones, desc='user_visit'):
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
    # print(visits)
    return visits
    '''
    [datetime.datetime(2023, 11, 14, 7, 45, 33), datetime.datetime(2023, 11, 14, 7, 45, 36),]
    '''

# 티켓이 있는 사용자만 추출하기
def filter_ticketuser_phone(user_infos):
    ticketuser_phones = list()
    for info in tqdm(user_infos, desc='ticket_user'):
        if info[1] != 0:
            ticketuser_phones.append(info[0])
    # print(ticketuser_phones)
    return ticketuser_phones
    '''
    ['010-8882-1463', '010-4047-5702']
    '''

# ticket의 상세 개수 추출하기

def get_ticket_detail(phones, token):
    curl = "https://api.monpass.im/api/crm/users/phone/"
    ticket_info = list()
    for phone in tqdm(phones, desc='ticket_info'):
        url = curl + phone.replace('-','') + "/benefits/ticket"
        res_data = get_data(url, token)
        data1 = list()
        for res in res_data['data']:
            data2 = data1 + [res['name'], res['count'], res['exp_date']]
            data1 = data2
        ticket_info.append(data1)
    # print(ticket_info)
    return ticket_info
    '''
    [['1시간(아이) 정기', '1', '2049-10-25T15:00:00.000Z', '2시간(아이) 정기', '5', '2050-01-31T15:00:00.000Z'],]
    '''

def data_align(phones, tickets, visits, ticketinfos):
    data = list()
    for p, t, v, info in zip(phones, tickets, visits, ticketinfos):
        data1 = [p, t, v]
        data1.extend(info)
        data.append(data1)
    # print(data)
    return data
    '''
    [['010-8882-1463', 4, datetime.datetime(2023, 9, 8, 13, 1, 15), '2시간 정기 (1년기한)', '4', '2024-05-02T15:00:00.000Z'],]
    '''

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
    print(f">> token: {token}\n")
    enter_memberpage()

    # total_user_cnt = 2000
    total_user_cnt = int(get_total_user_cnt())
    print(f">> Total user count: {total_user_cnt}\n")

    more_click(total_user_cnt)

    # selenium보다 beautifulsoup이 속도가 더 빠름    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 전체 사용자에 대한 정보
    user_phones = get_phone(soup)
    print(f">> Phone count: {len(user_phones)}\n")
    
    if total_user_cnt != len(user_phones):
        print('>> Count dismatch')
        exit()

    user_ticket = get_ticket(user_phones, token)
    user_visit = get_visit(user_phones, token)

    total_ticket_cnt_1 = sum(user_ticket)
    print(f">> Total ticket count 1: {total_ticket_cnt_1}\n")

    if total_user_cnt != len(user_ticket):
        print('>> Count dismatch')
        exit()
    elif total_user_cnt != len(user_visit):
        print('>> Count dismatch')
        exit()
    
    user_info = list(zip(user_phones, user_ticket, user_visit))
    save_to_excel(user_info, f"total_{len(user_phones)}_{total_ticket_cnt_1}")

    # ticket을 가진 사용자에 대한 상세 정보
    ticketuser_phones = filter_ticketuser_phone(user_info)
    print(f'>> Ticket users: {len(ticketuser_phones)}\n')

    ticketuser_ticket = get_ticket(ticketuser_phones, token)
    ticketuser_visit = get_visit(ticketuser_phones, token)
    ticketuser_ticket_info = get_ticket_detail(ticketuser_phones, token)
 
    total_ticket_cnt_2 = sum(ticketuser_ticket)
    print(f">> Total ticket count 2: {total_ticket_cnt_2}\n")

    if len(ticketuser_phones) != len(ticketuser_ticket):
        print('>> Count dismatch')
        exit()
    elif len(ticketuser_phones) != len(ticketuser_ticket_info):
        print('>> Count dismatch')
        exit()
    
    ticketuser_info = data_align(ticketuser_phones, ticketuser_ticket,
                                  ticketuser_visit, ticketuser_ticket_info)

    save_to_excel(ticketuser_info, f"ticket_{len(ticketuser_phones)}_{total_ticket_cnt_2}")
    
    driver.quit()

    sec = time.time() - start
    print(timedelta(seconds=sec))
    
    

    
