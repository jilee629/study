from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import tomllib
import time
import requests

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

def get_ticket(phone, token):
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    curl = "https://osio-api.peoplcat.com/shop/osio/user/search?type=phone&phone="
    url = curl + phone.replace('-', '')
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    res_data = res.json()
    ticket = filter_ticket(res_data)
    return ticket

def filter_ticket(data):
    ticket = list()
    for d in data['shop_users'][0]['user_osio_data']:
        ticket.append(d['shop_osio_product_name'])
        ticket.append(d['user_osio_data_value'])
        ticket.append(d['expiry_date'])
    return ticket

def save_to_excel(data):
    df = pd.DataFrame(data)
    df.index += 1
    t = datetime.now()
    fdate = t.strftime("%Y-%m-%d-%H-%M")
    df.to_excel(f"{fdate}_total_{len(data)}.xlsx", engine='openpyxl')

if __name__ == "__main__":

    start = datetime.now()
    
    credit = get_credit()
    driver = get_driver()
    page_login(credit[0], credit[1])
    token = get_token()
    
    today = datetime.now().strftime('%Y%m%d')
    df = pd.read_excel(today + "_점핑몬스터 미사점_고객정보.xlsx")
    list_cs = df[['전화번호','잔여 오티켓']].values.tolist()

    cs_info = list()
    for cs in tqdm(list_cs):
        info = list(cs)
        if cs[1] != 0:
            info.extend(get_ticket(cs[0], token))
        info.insert(1, len(cs[0]))
        cs_info.append(info)

    save_to_excel(cs_info)
    driver.quit()

    sec = datetime.now() - start
    print(f"Elapsed time : {timedelta(seconds=sec)}")