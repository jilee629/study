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
    res_token = driver.execute_script("return localStorage.getItem('token')")
    return res_token

def enter_memberpage():
    driver.get('https://partner.monpass.im/member')
    time.sleep(2)
    return

def more_click(total_user):
    for i in tqdm(range(50, int(total_user), 50), desc='more_click'):
        driver.find_element(By.CSS_SELECTOR, '.sc-cBdUnI.fBYDFC').click()
    time.sleep(2)
    return

def total_user_cnt():
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
def get_user_phone(soup):
    phone = soup.select('.ui-repeat.sc-cSHVUG.keecsQ > a > p > strong')
    phones = [p.text for p in phone]
    '''
    ['010-4213-7811', '010-4031-7134']
    '''
    return phones
    
def get_ticket(phone, token):
    curl = "https://api.monpass.im/api/crm/users/phone/" 
    url = curl + phone.replace('-','') + "/"
    res_data = get_data(url, token)
    ticket = res_data['data']['ticket']
    return ticket

def get_visit(phone, token):
    curl = "https://api.monpass.im/api/crm/users/phone/"
    url = curl + phone.replace('-','') + "/" + "logs?page=1"
    res_data = get_data(url, token)
    try:
        vtime = str(res_data['data']['rows'][0]['time'])[0:10]
    except:
        # 전화번호만 등록되고 방문기록은 얺는 경우가 있음
        vtime = "0123456789"
        print(' ', phone, ': Server is not responding.')
    visit = datetime.utcfromtimestamp(int(vtime))
    return visit

def get_user_ticket(phones, token):
    tickets = list()
    for phone in tqdm(phones, desc='user_ticket'):
        tickets.append(get_ticket(phone, token))
    '''
    [0, 0]
    '''
    return tickets

def get_user_visit(phones, token):
    visits = list()
    for phone in tqdm(phones, desc='user_visit'):
        visits.append(get_visit(phone, token))
    '''
    [datetime.datetime(2023, 9, 17, 9, 54, 23), 
    datetime.datetime(2023, 9, 17, 9, 54, 26)]
    '''
    return visits

# 티켓이 있는 사용자만 추출하기
def get_ticket_user(user_infos):
    ticket_user_phones = list()
    for info in tqdm(user_infos, desc='ticket_user'):
        if info[1] != 0:
            ticket_user_phones.append(info[0])
    '''
    ['010-8882-1463', '010-4047-5702']
    '''
    return ticket_user_phones

# ticket의 상세 개수 추출하기

def get_user_ticket_info(phones, token):
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
    '''
    [['2시간 정기 (1년기한)', '4', '2024-05-02T15:00:00.000Z'],
    ['2시간 정기 (1년기한)', '5', '2024-05-01T15:00:00.000Z']]
    '''
    return ticket_info

def data_align(phones, tickets, visits, ticketinfos):
    data = list()
    for p, t, v, info in zip(phones, tickets, visits, ticketinfos):
        data1 = [p, t, v]
        data1.extend(info)
        data.append(data1)
    '''
    [['010-8882-1463', 4, datetime.datetime(2023, 9, 8, 13, 1, 15), '2시간 정기 (1년기한)', '4', '2024-05-02T15:00:00.000Z'], 
    ['010-4047-5702', 5, datetime.datetime(2023, 5, 3, 1, 9, 59), '2시간 정기 (1년기 한)', '5', '2024-05-01T15:00:00.000Z']]
    '''
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
    print(f">> token: {token}\n")
    enter_memberpage()

    # total_user = 200
    total_user = int(total_user_cnt())
    print(f">> Total users: {total_user}\n")

    more_click(total_user)

    # selenium보다 beautifulsoup이 속도가 더 빠름    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 전체 사용자에 대한 정보
    user_phones = get_user_phone(soup)
    print(f">> Phones: {len(user_phones)}\n")
    
    if total_user != len(user_phones):
        print('>> Count dismatch')
        exit()

    user_ticket = get_user_ticket(user_phones, token)
    user_visit = get_user_visit(user_phones, token)

    total_ticket_cnt_1 = sum(user_ticket)
    print(f">> Total ticket count 1: {total_ticket_cnt_1}\n")

    if total_user != len(user_ticket):
        print('>> Count dismatch')
        exit()
    elif total_user != len(user_visit):
        print('>> Count dismatch')
        exit()
    
    user_info = list(zip(user_phones, user_ticket, user_visit))
    '''
    [('010-4213-7811', 0, datetime.datetime(2023, 9, 17, 9, 54, 23)), 
    ('010-4031-7134', 0, datetime.datetime(2023, 9, 17, 9, 54, 26))]
    '''
    save_to_excel(user_info, f"total_{len(user_phones)}_{total_ticket_cnt_1}")


    # ticket을 가진 사용자에 대한 상세 정보
    ticket_user_phones = get_ticket_user(user_info)
    print(f'>> Ticket users: {len(ticket_user_phones)}\n')

    ticket_user_ticket = get_user_ticket(ticket_user_phones, token)
    ticket_user_visit = get_user_visit(ticket_user_phones, token)
    ticket_user_ticket_info = get_user_ticket_info(ticket_user_phones, token)
 
    total_ticket_cnt_2 = sum(ticket_user_ticket)
    print(f">> Total ticket count 2: {total_ticket_cnt_2}\n")

    if len(ticket_user_phones) != len(ticket_user_ticket):
        print('>> Count dismatch')
        exit()
    elif len(ticket_user_phones) != len(ticket_user_ticket_info):
        print('>> Count dismatch')
        exit()
    
    ticket_user_info = data_align(ticket_user_phones, ticket_user_ticket,
                                  ticket_user_visit, ticket_user_ticket_info)

    save_to_excel(ticket_user_info, f"ticket_{len(ticket_user_phones)}_{total_ticket_cnt_2}")
    
    driver.quit()

    sec = time.time() - start
    print(timedelta(seconds=sec))
    
    

    
