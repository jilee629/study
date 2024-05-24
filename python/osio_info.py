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


def fetch(url):
    time.sleep(0.5)
    http = urllib3.PoolManager()
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = http.request('GET', url, headers=headers)
    return response

def get_shop_user_no(phone):
	curl = "https://osio-api.peoplcat.com/shop/osio/user/search?type=phone&phone="
	url = curl + phone
	response = fetch(url)
	shop_user_no = response.json()['shop_users'][0]['shop_user_no']
	user_no = response.json()['shop_users'][0]['user_no']
	return str(shop_user_no), str(user_no)

def get_entry_datetime(shop_user_no):
	curl = "https://osio-api.peoplcat.com/shop/v2/user/entry/log?shop_user_no="
	url = curl + shop_user_no
	try:
		response = fetch(url)
		entry_datetime = response.json()['log'][0]['entry_datetime']
		return entry_datetime
	except:
		return None

def get_visit_count(user_no, shop_usre_no):
	curl = "https://osio-api.peoplcat.com/shop/user/summary/data?user_no="
	url = curl + user_no + "&shop_user_no=" + shop_usre_no
	response = fetch(url)
	visit_count = response.json()['visit_count']
	return str(visit_count)

now = datetime.now()
print(f'-> {now}')

start = datetime.now().timestamp()

display = Display(visible=0, size=(1024, 768))
display.start()

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
prefs = {"download.default_directory": "/root/study/tmp"}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)

credit = os.path.dirname(__file__) + '/credit.toml'
with open(credit, 'rb') as f:
    data = tomllib.load(f)
    username = data['osio']['username']
    password = data['osio']['password']

# login page
driver.get("https://osio-shop.peoplcat.com/login")
print(f'-> {driver.current_url}')
driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[1]/input').send_keys(username)
driver.find_element(By.XPATH, '//*[@id="root"]/form/div/div[2]/input').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="root"]/form/div/button').click()

# manager mode
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/button[2]').click()
print(f'-> {driver.current_url}')

# user infomation excel download 
driver.get("https://osio-shop.peoplcat.com/admin/users")
print(f'-> {driver.current_url}')
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div/div[1]/div[2]/button').click()
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/button').click()
driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/div/button[2]').click()
time.sleep(5)


# get token
token = driver.execute_script("return localStorage.getItem('access_token')")
print(f"-> Token: {token}")

today = time.strftime('%Y%m%d', time.localtime())
# df = pd.read_excel('../tmp/' + today + '_점핑몬스터 미사점_고객정보.xlsx', dtype = 'str')
df = pd.read_excel('../tmp/' + today + '_점핑몬스터 미사점_고객정보.xlsx', dtype = 'str', nrows = 5)

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
fdate = now.strftime("%Y%m%d_%H%M")
fname = os.path.dirname(__file__) + '/../tmp/' + fdate + '.xlsx'
df.to_excel(fname, engine='openpyxl')

print(f"-> Elapsed time : {timedelta(seconds=datetime.now().timestamp() - start)}")

driver.quit()
display.stop()




