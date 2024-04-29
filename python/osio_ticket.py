from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import tomllib
import requests
from tqdm import tqdm
import time
from datetime import datetime, timedelta


def get_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("headless")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_credit():
    try:
        with open('python/credit.toml', 'rb') as f:
            data = tomllib.load(f)
            username = data['osio']['username']
            password = data['osio']['password']
    except:
        username = input('Your ID: ')
        password = input('Password: ')
    return [username, password]

def page_login(id, passwd):
    driver.get("https://osio-shop.peoplcat.com/login")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="아이디를 입력해 주세요."]').send_keys(id)
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="비밀번호를 입력해 주세요."]').send_keys(passwd)
    driver.find_element(By.CSS_SELECTOR, '.Button-sc-mznq07-0.LoginPage___StyledButton-sc-1ag2zbl-9.jVJpZh.hNBWCz').click()
    time.sleep(1)
    return

def get_token():
    token = driver.execute_script("return localStorage.getItem('access_token')")
    print(f"-> Token: {token}")
    return token

def send_query(url):
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def get_shop_user_no(data):
    url = "https://osio-api.peoplcat.com/shop/osio/user/search?type=phone&phone=" + str(data)
    res_data = send_query(url)
    shop_user_no = res_data['shop_users'][0]['shop_user_no']
    return shop_user_no

def get_entry_time(data):
    url = "https://osio-api.peoplcat.com/shop/v2/user/entry/log?shop_user_no=" + str(data)
    res_data = send_query(url)
    try:
        return res_data['log'][0]['entry_datetime']
    except:
        return None

def get_last_visit(data):
    last_visit = list()
    for phone in tqdm(data):
        shop_user_no = get_shop_user_no(phone)
        entry_time = get_entry_time(shop_user_no)
        last_visit.append(entry_time)
    return last_visit

def save_to_excel(data):
    df = pd.DataFrame(data)
    df.index += 1
    fdate = datetime.now().strftime("%Y%m%d%H%M")
    df.to_excel(f"{fdate}.xlsx", engine='openpyxl')


if __name__ == "__main__":

    start = time.time()
    
    driver = get_driver()
    credit = get_credit()
    page_login(credit[0], credit[1])
    token = get_token()
    
    today = time.strftime('%Y%m%d', time.localtime())
    df = pd.read_excel(today + '_점핑몬스터 미사점_고객정보.xlsx', dtype = 'str')

    cs_phone = df['전화번호'].values.tolist()
    cs_ticket_name = df['오시오명'].values.tolist()
    cs_ticket_count = df['오시오 잔여값'].values.tolist()
    cs_ticket_expired = df['오시오 만료일'].values.tolist()
    cs_last_visit = get_last_visit(cs_phone)

    cs_data = {
                'phone' : cs_phone,
                'ticket_name' : cs_ticket_name,
                'ticket_count' : cs_ticket_count,
                'ticket_expired' : cs_ticket_expired,
                'last_visited' : cs_last_visit,
            }

    print("lenth : ", 
          len(cs_data['phone']),
          len(cs_data['ticket_name']),
          len(cs_data['ticket_count']),
          len(cs_data['ticket_expired']),
          len(cs_data['last_visited']),
          )

    save_to_excel(cs_data)
    driver.quit()

    delta = time.time() - start
    print(f"-> Elapsed time : {timedelta(seconds=delta)}")