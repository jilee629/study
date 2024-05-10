from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import tomllib
from tqdm import tqdm
import time
from datetime import datetime
import urllib3

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

def fetch(url):
    time.sleep(0.5)
    http = urllib3.PoolManager()
    headers = {
        'Authorization': 'Bearer ' + token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    }
    response = http.request('GET', url, headers=headers)
    return response

def get_shop_user_no(phone):
    url = "https://osio-api.peoplcat.com/shop/osio/user/search?type=phone&phone=" + phone
    response = fetch(url)
    shop_user_no = response.json()['shop_users'][0]['shop_user_no']
    user_no = response.json()['shop_users'][0]['user_no']
    return str(shop_user_no), str(user_no)

def get_entry_datetime(shop_user_no):
    url = "https://osio-api.peoplcat.com/shop/v2/user/entry/log?shop_user_no=" + shop_user_no
    try:
        response = fetch(url)
        entry_datetime = response.json()['log'][0]['entry_datetime']
        return entry_datetime
    except:
        return None

def get_visit_count(user_no, shop_usre_no):
    url = "https://osio-api.peoplcat.com/shop/user/summary/data?user_no=" + user_no + "&shop_user_no=" + shop_usre_no
    response = fetch(url)
    visit_count = response.json()['visit_count']
    return str(visit_count)

if __name__ == "__main__":

    start = time.time()

    driver = get_driver()
    credit = get_credit()
    page_login(credit[0], credit[1])
    token = get_token()
    driver.quit()

    today = time.strftime('%Y%m%d', time.localtime())
    # df = pd.read_excel(today + '_점핑몬스터 미사점_고객정보.xlsx', dtype = 'str')
    df = pd.read_excel(today + '_점핑몬스터 미사점_고객정보.xlsx', dtype = 'str', nrows = 10)

    cs_phone = df['전화번호'].values.tolist()
    cs_ticket_name = df['오시오명'].values.tolist()
    cs_ticket_count = df['오시오 잔여값'].values.tolist()
    cs_ticket_expired = df['오시오 만료일'].values.tolist()
    
    cs_shop_user_no = list()
    cs_user_no = list()
    for phone in tqdm(cs_phone, desc='user_no'):
        result = get_shop_user_no(phone)
        cs_shop_user_no.append(result[0])
        cs_user_no.append(result[1])
        
    cs_entry_datatime = list()
    for shop_user_no in tqdm(cs_shop_user_no, desc='entry_datatime'):
        cs_entry_datatime.append(get_entry_datetime(shop_user_no))
        
    cs_visit_count = list()
    for user_no, shop_user_no in tqdm(zip(cs_user_no, cs_shop_user_no), total = len(cs_user_no), desc='visit_count'):
        cs_visit_count.append(get_visit_count(user_no, shop_user_no))
        
    cs_data = {
                'phone' : cs_phone,
                'osio_name' : cs_ticket_name,
                'osio_count' : cs_ticket_count,
                'expired' : cs_ticket_expired,
                'shop_user_no' : cs_shop_user_no,
                'user_no' : cs_user_no,
                'entry_datetime' : cs_entry_datatime,
                'visit_count' : cs_visit_count,
            }
      
    [print(f"{key} : {len(value)}") for key, value in cs_data.items()]

    df = pd.DataFrame(cs_data)
    fdate = datetime.now().strftime("%Y%m%d_%H%M")
    df.to_excel(f"{fdate}.xlsx", engine='openpyxl')

    print(f"-> Elapsed time : {time.time() - start}")
        
    # [print(val) for val in cs_data.values()]
    

