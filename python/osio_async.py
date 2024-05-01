from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import tomllib
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

async def shop_user_no(session, url, i):
    async with session.get(url, headers=headers) as response:
        start = time.time()
        response = await response.json()
        shop_user_no = response['shop_users'][0]['shop_user_no']
        print(f"Task shop_user_no-{i} : {timedelta(seconds=(time.time() - start))}")
        return shop_user_no

async def main_shop_user_no(cs_phone):
    async with aiohttp.ClientSession() as session:
        tasks = list()
        for i, phone in enumerate(cs_phone):
            url = "https://osio-api.peoplcat.com/shop/osio/user/search?type=phone&phone=" + phone
            tasks.append(shop_user_no(session, url, i))
        result = await asyncio.gather(*tasks)
        return result

async def entry_datetime(session, url, i):
    async with session.get(url, headers=headers) as response:
        start = time.time()
        response = await response.json()
        try:
            entry_datetime = response['log'][0]['entry_datetime']
            print(f"Task entry_datetime-{i} : {timedelta(seconds=(time.time() - start))}")
            return entry_datetime
        except:
            return None

async def main_entry_datetime(cs_shop_user_no):
    async with aiohttp.ClientSession() as session:
        tasks = list()
        for i, shop_user_no in enumerate(cs_shop_user_no):
            url = "https://osio-api.peoplcat.com/shop/v2/user/entry/log?shop_user_no=" + str(shop_user_no)
            tasks.append(entry_datetime(session, url, i))
        result = await asyncio.gather(*tasks)
        return result

async def user_no(session, url, i):
    async with session.get(url, headers=headers) as response:
        start = time.time()
        response = await response.json()
        user_no = response['shop_users'][0]['user_no']
        print(f"Task user_no-{i} : {timedelta(seconds=(time.time() - start))}")
        return user_no

async def main_user_no(cs_phone):
    async with aiohttp.ClientSession() as session:
        tasks = list()
        for i, phone in enumerate(cs_phone):
            url = "https://osio-api.peoplcat.com/shop/osio/user/search?type=phone&phone=" + phone
            tasks.append(user_no(session, url, i))
        result = await asyncio.gather(*tasks)
        return result

async def visit_count(session, url, i):
    async with session.get(url, headers=headers) as response:
        start = time.time()
        response = await response.json()
        visit_count = response['visit_count']
        print(f"Task visit_count-{i} : {timedelta(seconds=(time.time() - start))}")
        return visit_count
                                
async def main_visit_count(cs_user_no, cs_shop_user_no):
    async with aiohttp.ClientSession() as session:
        tasks = list()
        for i, cs_zip in enumerate(zip(cs_user_no, cs_shop_user_no)):
            url = url = "https://osio-api.peoplcat.com/shop/user/summary/data?user_no=" + str(cs_zip[0]) + "&shop_user_no=" + str(cs_zip[1])
            tasks.append(visit_count(session, url, i))
        result = await asyncio.gather(*tasks)
        return result

start = time.time()

driver = get_driver()
credit = get_credit()
page_login(credit[0], credit[1])
token = get_token()

today = time.strftime('%Y%m%d', time.localtime())
df = pd.read_excel(today + '_점핑몬스터 미사점_고객정보.xlsx', dtype = 'str')
# df = pd.read_excel(today + '_점핑몬스터 미사점_고객정보.xlsx', dtype = 'str', nrows = 10)

cs_phone = df['전화번호'].values.tolist()
cs_ticket_name = df['오시오명'].values.tolist()
cs_ticket_count = df['오시오 잔여값'].values.tolist()
cs_ticket_expired = df['오시오 만료일'].values.tolist()

headers = {
    'Authorization': 'Bearer ' + token,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
}

cs_shop_user_no = asyncio.run(main_shop_user_no(cs_phone))
cs_entry_datetime = asyncio.run(main_entry_datetime(cs_shop_user_no))

cs_user_no = asyncio.run(main_user_no(cs_phone))
cs_visit_count = asyncio.run(main_visit_count(cs_user_no, cs_shop_user_no))

cs_data = {
            'phone' : cs_phone,
            'osio_name' : cs_ticket_name,
            'osio_count' : cs_ticket_count,
            'osio_expired' : cs_ticket_expired,
            'shop_user_no' : cs_shop_user_no,
            'entry_datetime' : cs_entry_datetime,
            'user_no' : cs_user_no,
            'visit_count' : cs_visit_count,
        }

driver.quit()
delta = time.time() - start
print(f"-> Elapsed time : {timedelta(seconds=delta)}")

[print(f"{key} : {len(value)}") for key, value in cs_data.items()]

df = pd.DataFrame(cs_data)
fdate = datetime.now().strftime("%Y%m%d%H%M")
df.to_excel(f"{fdate}.xlsx", engine='openpyxl')

# [print(val) for val in cs_data.values()]








