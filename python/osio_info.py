#!/usr/bin/env python

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import pandas as pd
import tomllib
from tqdm import tqdm
import time
from datetime import datetime, timedelta
import urllib3
import os

def get_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {"download.default_directory": "/home/ubuntu/log"})
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver

def get_credit():
    credit = os.path.dirname(__file__) + '/credit.toml'
    with open(credit, 'rb') as f:
        data = tomllib.load(f)
        username = data['osio']['username']
        password = data['osio']['password']
    return username, password

def enter_login(username, password):
    # login page
    url = "https://osio-shop.peoplcat.com/login"
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[1]/input').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[2]/input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="root"]/form/div/button').click()
    # manager mode
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/button[2]').click()
    return

def download_csinfo():
    driver.get("https://osio-shop.peoplcat.com/admin/users")
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div[1]/button').click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/button').click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/button[2]').click()
    time.sleep(5)
    return

def get_token():
    token = driver.execute_script("return localStorage.getItem('access_token')")
    print(f"-> Token: {token}")
    return token

def get_cs_phone_len(cs_phone, ):
    cs_phone_len = list()
    for phone in tqdm(cs_phone, desc='phone_len'):
        cs_phone_len.append(len(phone))
    return cs_phone_len

def save_data(cs_data):
    df = pd.DataFrame(cs_data)
    fname = '/home/ubuntu/log/' + now.strftime('%Y%m%d_%H%M') + '_점핑몬스터 미사점_고객정보.xlsx'
    df.to_excel(fname, engine='openpyxl')
    return

def fetch(url):
    time.sleep(0.5)
    http = urllib3.PoolManager()
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = http.request('GET', url, headers=headers)
    return response


def get_cs_user_info(phone):
    # 고객정보 - 검색
	curl = "https://osio-api.peoplcat.com/shop/osio/user/"
	url = curl + "search?type=phone&phone=" + phone
	response = fetch(url)
	shop_user_no = response.json()['shop_users'][0]['shop_user_no']
	user_no = response.json()['shop_users'][0]['user_no']
	return str(shop_user_no), str(user_no)

def get_user_no(cs_phone):
    cs_shop_user_no = list()
    cs_user_no = list()   
    for phone in tqdm(cs_phone, desc='user_no'):
        result = get_cs_user_info(phone)
        cs_shop_user_no.append(result[0])
        cs_user_no.append(result[1])
    return cs_shop_user_no, cs_user_no


def get_cs_entry(shop_user_no):
	# 고객정보 - 입/퇴장
    curl = "https://osio-api.peoplcat.com/shop/v2/user/entry/"
    url = curl + "log?shop_user_no=" + shop_user_no
    record = response.json()['log'][0]['record']
    try:
		response = fetch(url)
		entry_datetime = response.json()['log'][0]['entry_datetime']
		return record, entry_datetime
	except:
		return record, None

def get_cs_manage(cs_shop_user_no):
    cs_record = list()
    cs_entry_datatime = list()
    for shop_user_no in tqdm(cs_shop_user_no, desc='entry_datatime'):
        # cs_entry_datatime.append(get_cs_entry(shop_user_no))
        record, entry_datetime = get_cs_entry(shop_user_no)
        cs_record.append(record)
        cs_entry_datatime(entry_datetime)
    return cs_record, cs_entry_datatime


    

def get_visit_count(user_no, shop_usre_no):
	# 고객관리 - 고객정보
    curl = "https://osio-api.peoplcat.com/shop/user/summary/"
	url = curl + "data?user_no=" + user_no + "&shop_user_no=" + shop_usre_no
	response = fetch(url)
	visit_count = response.json()['visit_count']
	return str(visit_count)

def get_cs_visit_count(cs_user_no, cs_shop_user_no):
    cs_visit_count = list()
    for user_no, shop_user_no in tqdm(zip(cs_user_no, cs_shop_user_no), total = len(cs_user_no), desc='visit_count'):
        cs_visit_count.append(get_visit_count(user_no, shop_user_no))
    return cs_visit_count










if __name__ == "__main__":

    display = Display(visible=0, size=(1024, 768))
    display.start()

    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S %A"))
    start = datetime.now().timestamp()

    driver = get_driver()
    username, password = get_credit()
    enter_login(username, password) 
    download_csinfo()
    token = get_token()

    csfile = '/home/ubuntu/log/' + now.strftime('%Y%m%d') + '_점핑몬스터 미사점_고객정보.xlsx'
    # df = pd.read_excel(csfile, dtype = 'str')
    df = pd.read_excel(csfile, dtype = 'str', nrows = 100)

    cs_phone = df['전화번호'].values.tolist()
    cs_phone_len = get_cs_phone_len(cs_phone)
    cs_ticket_name = df['오시오명'].values.tolist()
    cs_ticket_count = df['오시오 잔여값'].values.tolist()
    cs_ticket_expired = df['오시오 만료일'].values.tolist()
    cs_shop_user_no, cs_user_no = get_user_no(cs_phone)
    cs_record, cs_entry_datatime = get_cs_entry(cs_shop_user_no)
    cs_visit_count = get_cs_visit_count(cs_user_no, cs_shop_user_no)
    cs_data = {
                'phone' : cs_phone,
                'phone_len' : cs_phone_len,
                'osio' : cs_ticket_name,
                'count' : cs_ticket_count,
                'expired' : cs_ticket_expired,
                'record' : cs_record,
                'entry' : cs_entry_datatime,
                'visit' : cs_visit_count,
            } 

    [print(f"{key} : {len(value)}") for key, value in cs_data.items()]
    # save_data(cs_data)
    print(f"-> Elapsed time : {timedelta(seconds=datetime.now().timestamp() - start)}")

    driver.quit()
    display.stop()

