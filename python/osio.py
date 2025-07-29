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
import os, time, tomllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log_dir = "/home/ubuntu/log/"

def get_driver():
    options = Options()
    if os.name != 'nt':
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,1024")
        # options.add_argument("--remote-debugging-pipe")
        options.add_experimental_option("prefs", {"download.default_directory": log_dir})
        service = Service(ChromeDriverManager().install())
    else:
        options.add_argument("--start-maximized")
        service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver

def get_credential():
    credential = os.path.dirname(__file__) + '/credentials.toml'
    with open(credential, 'rb') as f:
        data = tomllib.load(f)
        username = data['osio']['username']
        password = data['osio']['password']
    return username, password

def popup_close(driver, cnt):
    for i in range(cnt, 0, -1):
        print(f'{i} Popup is opened')
        driver.find_element(By.XPATH, f'//*[@id="root"]/div[{i}]/div/div/div/div/div[3]/div').click()
        driver.find_element(By.XPATH, f'//*[@id="root"]/div[{i}]/div/div/div/div/div[3]/button').click()
    return

def enter_login(driver, username, password):
    driver.get("https://osio-shop.peoplcat.com/login")

    # popup window
    try:
        if driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div'):
            popup_close(driver, 2)
        elif driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div'):
            popup_close(driver, 1)
        else:
            print('popup is not opened')
    except:
        pass

    # login
    username_input = driver.find_element(By.XPATH, '//*[@placeholder="아이디를 입력해 주세요."]')
    username_input.send_keys(username)
    password_input = driver.find_element(By.XPATH, '//*[@placeholder="비밀번호를 입력해 주세요."]')
    password_input.send_keys(password)
    submit_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
    # submit_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]'))
    # )
    submit_button.click()

    # select manager
    manager_button = driver.find_element(By.XPATH, '//button[contains(., "manager")]')
    manager_button.click()
    return

def exit_user(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/settings")
    exit_button = driver.find_element(By.XPATH, '//button[contains(., "고객 전체 퇴장")]')
    exit_button.click()
    confirm_button = driver.find_element(By.XPATH, '//button[text()="확인"]')
    confirm_button.click()
    time.sleep(3)
    print('exit_user is OK.')
    return

def get_count(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/entry")
    adult = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/header/div[2]/div/span[2]').text
    child = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/header/div[2]/div/span[4]').text
    print(f'-> Adult: {adult}, Child: {child}')
    return

def download_csinfo(driver):
    driver.get("https://osio-shop.peoplcat.com/admin/users")
    cs_download_button = driver.find_element(By.XPATH, '//button[text()="고객 다운로드"]')
    cs_download_button.click()
    agree_button = driver.find_element(By.XPATH, '//button[contains(., "위 내용에 동의합니다")]')
    agree_button.click()
    download_button = driver.find_element(By.XPATH, '//button[text()="다운로드"]')
    download_button.click()
    time.sleep(10)
    print('download_csinfo is OK.')
    return

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

def write_phone_len(file_name):
    old_file = log_dir + file_name
    df = pd.read_excel(old_file, dtype = 'str')
    df['전화번호길이'] = df['전화번호'].str.len()
    new_file = log_dir + "len_" + file_name
    df.to_excel(new_file, engine='openpyxl')
    print(f'writing {new_file} is OK.')

def upload_file(file_name, mtype = None):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    local_file_path = log_dir + file_name
    if mtype == "xlsx":
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        mimetype='text/plain'

    media = MediaFileUpload(local_file_path, mimetype=mimetype, resumable=True)
    drive_file_name = file_name
    file_metadata = {'name': drive_file_name,
                    'parents': ['1Wwb3CYQ7OnCp5hWboVXELPxbxtAbXP9R']
                    }
    file = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    file.get('id')
    print(f'uploading {file_name} is OK.')
    return 

