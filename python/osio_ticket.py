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
import asyncio
import aiohttp

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def query_shop_user_no(phone):
    url = "https://osio-api.peoplcat.com/shop/osio/user/search?type=phone&phone=" + phone
    res_data = send_query(url)
    shop_user_no = res_data['shop_users'][0]['shop_user_no']
    return str(shop_user_no)

def query_user_no_shop_user_no(phone):
    url = "https://osio-api.peoplcat.com/shop/osio/user/search?type=phone&phone=" + phone
    res_data = send_query(url)
    shop_user_no = res_data['shop_users'][0]['shop_user_no']
    user_no = res_data['shop_users'][0]['user_no']
    return str(user_no), str(shop_user_no)

def query_visit_count(user_no, shop_user_no):
    url = "https://osio-api.peoplcat.com/shop/user/summary/data?user_no=" + user_no + "&shop_user_no=" + shop_user_no
    res_data = send_query(url)
    return res_data['visit_count']

def query_entry_datetime(shop_user_no):
    url = "https://osio-api.peoplcat.com/shop/v2/user/entry/log?shop_user_no=" + shop_user_no
    res_data = send_query(url)
    return res_data['log'][0]['entry_datetime']

def get_visit_count(phone):
    visit_count = list()
    for p in tqdm(phone, desc='visit_count'):
        user_no , shop_user_no = query_user_no_shop_user_no(p)
        user_visit_count = query_visit_count(user_no, shop_user_no)
        visit_count.append(user_visit_count)
    return visit_count

def get_entry_datetime(visit_count, phone):
    last_visit = list()
    for v, p in zip(tqdm(visit_count, desc='entry_datetime'), phone):
        if v == 0:
            last_visit.append(None)
        else:
            shop_user_no= query_shop_user_no(p)
            entry_time = query_entry_datetime(shop_user_no)
            last_visit.append(entry_time)
    return last_visit


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
    cs_visit_count = get_visit_count(cs_phone)
    cs_entry_datetime = get_entry_datetime(cs_visit_count, cs_phone)
    cs_data = {
                'phone' : cs_phone,
                'ticket_name' : cs_ticket_name,
                'ticket_count' : cs_ticket_count,
                'ticket_expired' : cs_ticket_expired,
                'visit_count' : cs_visit_count,
                'entry_datetime' : cs_entry_datetime,
            }
    [print(len(val)) for val in cs_data.values()]
    driver.quit()

    df = pd.DataFrame(cs_data)
    fdate = datetime.now().strftime("%Y%m%d%H%M")
    df.to_excel(f"{fdate}.xlsx", engine='openpyxl')
    
    delta = time.time() - start
    print(f"-> Elapsed time : {timedelta(seconds=delta)}")

