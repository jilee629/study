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
    token = driver.execute_script("return localStorage.getItem('token')")
    print(f"token: {token}")
    return token

# member list 추출
def get_phone_list(soup):
    phone = soup.select('.ui-repeat.sc-cSHVUG.keecsQ > a > p > strong')
    phone_list = get_phone(phone)
    return phone_list

# 전화번호 추출
def get_phone(phone_list):
    phones = [m.text for m in phone_list]
    return phones

# 티켓이 있는 사용자만 티켓개수 추출하기
def get_user_ticket(tickets):
    user_tickets = []
    for t in tickets:
        if t[1] != 0:
            user_tickets.append(t)
    return user_tickets

def get_data(url, token):
    headers = {
        'token': token,
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    res_data = res.json()
    return res_data

# 사용자 ticket 정보 추출하기
def get_ticket_data(phones, token):
    global_url = "https://api.monpass.im/api/crm/users/phone/"
    ticket = []
    visit = []
    for phone in tqdm(phones):
        url = global_url + phone.replace('-','') + "/"
        # ticket 개수
        res_data = get_data(url, token)
        ticket.append(res_data['data']['ticket'])
        # 방문 시간
        url = url + "logs?page=1"
        res_data = get_data(url, token)
        # vtime = str(res_data['data']['rows'][0]['time'])[0:10]
        try:
            vtime = str(res_data['data']['rows'][0]['time'])[0:10]
        except:
            vtime = "0000000000"
        visit.append(datetime.utcfromtimestamp(int(vtime)))
    return list(zip(phones, ticket, visit))

# ticket의 상세 개수 추출하기
def get_detail_user_ticket(phones, token):
    global_url = "https://api.monpass.im/api/crm/users/phone/"
    data = []
    for phone, ticket, visit in phones:
        url = global_url + phone.replace('-','') + "/benefits/ticket"
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


if __name__ == "__main__":
    url = "https://partner.monpass.im/"
    id = input('Your ID: ')
    passwd = input('Password: ')
    # id = ''
    # passwd = ''

    driver = get_driver()
    page_login(url, id, passwd)
    token = get_token()

    more_click()
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    # 명단에서 phone 번호만 추출하기
    phone_list = get_phone_list(soup)

    # 중간확인
    total_user_cnt = soup.select_one('.sc-iFMziU.gNKmAv').text
    print(f"Total User Count: {total_user_cnt[0:-1]}")
    print(f"Number of phone: {len(phone_list)}")
    if int(total_user_cnt[0:-1]) != len(phone_list):
        print("User count and phone list count are dismatched")
        exit()
   
    # 전체 사용자에 대해 ticket 개수 조회
    all_user_ticket_data = get_ticket_data(phone_list, token)

    # ticket 가진 사용자만 골라내기
    ticket_user_list = get_user_ticket(all_user_ticket_data)
    print(f"Ticket user count: {len(ticket_user_list)}")
    # ticket 가진 사용자만 종류별 티켓개수 추출하기
    ticket_user_data = get_detail_user_ticket(ticket_user_list, token)
    
    # 브라우저 닫기
    driver.quit()

    #엑셀 저장
    col = None
    save_to_excel(ticket_user_data, col, f"ticket_{len(ticket_user_data)}")
    # col = ['Phone', 'Total ticket']
    save_to_excel(all_user_ticket_data, col, f"total_{len(all_user_ticket_data)}")

    
