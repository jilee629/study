from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
from tqdm import tqdm
import pandas as pd

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
    # 회원관리 페이지
    driver.get('https://partner.monpass.im/member')
    time.sleep(1)
    return

def more_click():
    t = 1
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, '.sc-cBdUnI.fBYDFC').click()
            # print(".", end="")
            print(t, "page reading is done.")
            t += 1
            time.sleep(.1)
        except:
            # print("")
            print("No more page")
            break

def get_token():
    res_token = driver.execute_script("return localStorage.getItem('token')")
    print(f"token: {res_token}")
    return res_token

# phone list 추출
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
        url = url + "logs?page=1"
        res_data = get_data(url, token)
        try:
            vtime = str(res_data['data']['rows'][0]['time'])[0:10]
        except:
            # 전화번호만 등록되고 방문기록은 얺는 경우가 있음
            vtime = "0123456789"
            print(str(phone), ': Server is not responding.')
        visit.append(datetime.utcfromtimestamp(int(vtime)))

    return list(zip(phones, ticket, visit))

# ticket의 상세 개수 추출하기
def get_ticket_info(user, token):
    curl = "https://api.monpass.im/api/crm/users/phone/"
    data = []
    for phone, ticket, visit in tqdm(user):
        url = curl + phone.replace('-','') + "/benefits/ticket"
        res_data = get_data(url, token)
        d1 = (phone, ticket, visit)
        for r in res_data['data']:
            d2 = d1 + (r['name'], r['count'], r['exp_date'])
            d1 = d2
        data.append(d2)
    return data
  
def save_to_excel(data, prefix):
    col = None
    t = datetime.now()
    df = pd.DataFrame(data, columns=col)
    df.index += 1
    fdate = t.strftime("%Y-%m-%d-%H-%M")
    df.to_excel(f"{fdate}_{prefix}.xlsx", header=True, engine='openpyxl')


if __name__ == "__main__":
 
    credit = get_credit()
    driver = get_driver()

    url = "https://partner.monpass.im/"
    page_login(url, credit[0], credit[1])
    token = get_token()

    more_click()
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
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

    # ticket 가진 사용자만 골라내서 티켓 종류별로 추출
    ticket_user = get_ticket_user(all_user_info)
    print(f"Ticket user count: {len(ticket_user)}")
    ticket_info = get_ticket_info(ticket_user, token)
    
    driver.quit()

    save_to_excel(ticket_info, f"ticket_{len(ticket_info)}")
    save_to_excel(all_user_info, f"total_{len(all_user_info)}")

    
