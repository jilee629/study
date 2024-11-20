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
    time.sleep(10)
    return

def get_token():
    token = driver.execute_script("return localStorage.getItem('access_token')")
    print(f"-> Token: {token}")
    return token

def save_data(cs_info, columns):
    df = pd.DataFrame(cs_info, columns=columns)
    fname = '/home/ubuntu/log/' + now.strftime('%Y%m%d_%H%M') + '_점핑몬스터 미사점_고객정보.xlsx'
    df.to_excel(fname, engine='openpyxl')
    return

def fetch(url):
    http = urllib3.PoolManager()
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = http.request('GET', url, headers=headers)
    time.sleep(0.5)
    return response

def get_sid_uid(phone):
    # 고객정보 - 검색
	curl = "https://osio-api.peoplcat.com/shop/osio/user/"
	url = curl + "search?type=phone&phone=" + phone
	response = fetch(url)
	shop_user_no = response.json()['shop_users'][0]['shop_user_no']
	user_no = response.json()['shop_users'][0]['user_no']
	return str(shop_user_no), str(user_no)

def get_lastvisit(shop_user_no):
	# 고객정보 - 입/퇴장
    curl = "https://osio-api.peoplcat.com/shop/v2/user/entry/"
    url = curl + "log?shop_user_no=" + shop_user_no
    response = fetch(url)
    try:
        entry = response.json()['log'][0]['entry_datetime']
    except:
        entry = None
    return entry

def get_visitcount(user_no, shop_usre_no):
	# 고객관리 - 고객정보
    curl = "https://osio-api.peoplcat.com/shop/user/summary/"
    url = curl + "data?user_no=" + user_no + "&shop_user_no=" + shop_usre_no
    response = fetch(url)
    visit_count = response.json()['visit_count']
    return str(visit_count)

if __name__ == "__main__":

    display = Display(visible=0, size=(1024, 768))
    display.start()

    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S %A"))
    start = datetime.now().timestamp()

    driver = get_driver()
    username, password = get_credit()
    enter_login(username, password) 
    token = get_token()
    # download_csinfo()
    csfile = '/home/ubuntu/log/' + now.strftime('%Y%m%d') + '_점핑몬스터 미사점_고객정보.xlsx'
    
    # df = pd.read_excel(csfile, dtype = 'str')
    df = pd.read_excel(csfile, dtype = 'str', nrows = 3)

    cs_info = df.values.tolist()
    for cs in tqdm(cs_info):
        phone = cs[1]

        # 전화번호 길이
        cs.append(len(phone))
        
        # shop_user_no, user_no
        shop_user_no, user_no = get_sid_uid(phone)

        # 마지막 방문일
        lastvisit = get_lastvisit(shop_user_no)
        cs.append(lastvisit)

        # 방문 회수
        visitcount = get_visitcount(user_no, shop_user_no)
        cs.append(visitcount)

    # test
    #[print(cs) for cs in cs_info]

    # 저장
    columns = [
                '이름','전화번호','생일','기록',
                '오시오명','오티켓','오티켓개수','오티켓만료일',
                '전화번호길이','방문일','방문회수'
                ]
    save_data(cs_info, columns)

    print(f"-> Elapsed time : {timedelta(seconds=datetime.now().timestamp() - start)}")
    driver.quit()
    display.stop()



