from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

import pandas as pd
import os, time, tomllib, requests
from datetime import datetime

log_dir = "/home/ubuntu/log/"

# webdriver

def get_driver():
    options = Options()
    if os.name != 'nt':
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {"download.default_directory": log_dir})
    else:
        # options.add_argument("--headless=new")
        pass
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-pipe")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)
    return driver

def get_credential():
    credential = os.path.dirname(__file__) + '/credentials.toml'
    with open(credential, 'rb') as f:
        data = tomllib.load(f)
        username = data['osio']['username']
        password = data['osio']['password']
    return username, password

def enter_login(driver, username, password):
    driver.get("https://osio-shop.peoplcat.com/login")
    time.sleep(1)

    # popup window
    try:
        for i in range(2):
            checkbox = driver.find_element(By.XPATH, '//p[text()="일주일간 보지 않기"]/ancestor::div[3]')
            checkbox.click()
            close_button = driver.find_element(By.XPATH, '//button[text()="닫기"]')
            close_button.click()
            time.sleep(1)
            print("POPUP CLOSED.")
    except:
        print("NO POPUP.")
        
    # login
    username_input = driver.find_element(By.XPATH, '//*[@placeholder="아이디를 입력해 주세요."]')
    username_input.send_keys(username)
    password_input = driver.find_element(By.XPATH, '//*[@placeholder="비밀번호를 입력해 주세요."]')
    password_input.send_keys(password)
    login_button = driver.find_element(By.XPATH, '//button[text()="로그인"]')
    login_button.click()
    time.sleep(1)

    # select manager
    manager_button = driver.find_element(By.XPATH, '//button[contains(., "manager")]')
    manager_button.click()
    time.sleep(1)
    return

def exit_user(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/settings")
    time.sleep(1)
    exit_button = driver.find_element(By.XPATH, '//button[contains(., "고객 전체 퇴장")]')
    exit_button.click()
    time.sleep(1)
    confirm_button = driver.find_element(By.XPATH, '//button[text()="확인"]')
    confirm_button.click()
    time.sleep(3)
    print('EXIT_USER IS OK.')
    return

def get_count(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/entry")
    time.sleep(1)
    adult = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/header/div[2]/div/span[2]').text
    child = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/header/div[2]/div/span[4]').text
    print(f'-> Adult: {adult}, Child: {child}')
    return

def download_csinfo(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/users")
    time.sleep(1)
    cs_download_button = driver.find_element(By.XPATH, '//button[text()="고객 다운로드"]')
    cs_download_button.click()
    time.sleep(1)
    agree_button = driver.find_element(By.XPATH, '//button[contains(., "위 내용에 동의합니다")]')
    agree_button.click()
    download_button = driver.find_element(By.XPATH, '//button[text()="다운로드"]')
    download_button.click()
    time.sleep(10)
    print('DOWNDLOAD_CSINFO IS OK.')
    return True

def delete_user(driver, phone):
    driver.get("https://osio-shop.peoplcat.com/admin/osio/search")
    time.sleep(1)
    phone_input = driver.find_element(By.XPATH, '//*[@placeholder="전화번호 입력 후 검색버튼을 눌러주세요."]')
    phone_input.send_keys(phone)
    search_button = driver.find_element(By.XPATH, '//button[contains(., "검색")]')
    search_button.click()
    time.sleep(1)
    delete_button = driver.find_element(By.XPATH, '//button[text()="회원탈퇴"]')
    delete_button.click()
    time.sleep(1)
    message_switch = driver.find_element(By.XPATH, '//span[text()="ON"]/ancestor::div[1]')
    message_switch.click()
    time.sleep(1)
    confirm_button = driver.find_element(By.XPATH, '//button[text()="확인"]')
    confirm_button.click()
    time.sleep(1)
    print(f"{phone} USER DELETED.")
    return


# request

def get_token(driver):
    token = driver.execute_script("return localStorage.getItem('access_token')")
    return token

def fetch(url, token):
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    response = requests.get(url, headers=headers)
    return response

def write_phone_len(file_name):
    old_file = log_dir + file_name
    df = pd.read_excel(old_file, dtype = 'str')
    df['전화번호길이'] = df['전화번호'].str.len()
    new_file = log_dir + "len_" + file_name
    df.to_excel(new_file, engine='openpyxl')
    print(f'writing {new_file} is OK.')

def get_user_data(phone, token):
    curl = "https://osio-api.peoplcat.com/shop/v2/user/search?type=phone"
    url = curl + "&phone=" + phone
    response = fetch(url, token)
    shop_user_no = response.json()['shop_users'][0]['shop_user_no']
    user_no = response.json()['shop_users'][0]['user_no']
    return shop_user_no, user_no

def get_user_summary(user_no, shop_user_no, token):
    curl = "https://osio-api.peoplcat.com/shop/user/summary/data"
    url = curl + "?user_no=" + str(user_no) + "&shop_user_no=" + str(shop_user_no)
    response = fetch(url, token)
    visit_count = response.json()['visit_count']
    len_osiodata = len(response.json()['user_osio_data'])
    if len_osiodata == 0:
        oticket = 0
    else:
        oticket = response.json()['user_osio_data'][0]['value']
    return visit_count, oticket

def get_user_log(shop_user_no, token):
    curl = "https://osio-api.peoplcat.com/shop/v2/user/entry/log"
    url = curl + "?shop_user_no=" + str(shop_user_no)
    response = fetch(url, token)
    try:
        entry = response.json()['log'][0]['entry_datetime']
    except:
        entry = None
    return entry


# google drive

def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None

    token_file = os.path.dirname(__file__) + '/token.json'
    credentials_file = os.path.dirname(__file__) + '/credentials.json'

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds

def create_drive_folder(folder_name):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
                    'name': folder_name,
                    "mimeType": "application/vnd.google-apps.folder",
                    'parents': ['1Wwb3CYQ7OnCp5hWboVXELPxbxtAbXP9R']
                    }

    file = service.files().create(body=file_metadata, fields="id").execute()
    folder_id = file.get("id")
    return folder_id

def upload_file(folder_id, file_name, mtype=None):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    local_file_path = log_dir + file_name
    if mtype == "xlsx":
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        mimetype='text/plain'

    media = MediaFileUpload(local_file_path, mimetype=mimetype, resumable=True)

    drive_file_name = file_name
    file_metadata = {
                    'name': drive_file_name,
                    'parents': [folder_id]
                    }

    file = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    file.get('id')
    print(f'UPLOADING {file_name} IS OK.')
    return True


# 
def print_datetime():
    now = datetime.now()
    print(f"\n{now.strftime('%Y-%m-%d %H:%M:%S %A')}")
    return
