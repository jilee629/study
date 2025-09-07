#!/usr/bin/env python3

from pyvirtualdisplay import Display
from datetime import datetime, timedelta
import osio
import os
import pandas as pd

phone = '''0104170026
0103425487
0109298105
0109382813
0105345979
0106687545
0106768874
0103742874
'''

if os.name != 'nt':
    display = Display(visible=0, size=(1920,1080))
    display.start()

    log_dir = "/home/ubuntu/log/"
    yesterday = datetime.now() - timedelta(days = 1)
    fdate = yesterday.strftime("%Y%m%d")
    file_name = "len_" + fdate + "_점핑몬스터 미사점_고객정보.xlsx"
    file_path = log_dir + file_name
    df = pd.read_excel(file_path, dtype = 'str')
    phone_list = df.loc[df['전화번호길이'] == '10'].values.tolist()
    print(phone_list)
else:
    # 데이타를 입력
    # phone_list = phone.splitlines()
    # print(pd.Series(phone_list))

    # 엑셀 파일을 입력
    file_path = os.path.dirname(__file__) + '/len_20250905_점핑몬스터 미사점_고객정보.xlsx'
    df = pd.read_excel(file_path, dtype = 'str')
    df_filter = df.loc[df['전화번호길이'] == '10']
    phone_list = df_filter["전화번호"].values.tolist()
    print(phone_list)

driver = osio.get_driver()
username, password = osio.get_credential()
osio.enter_login(driver, username, password)
token = osio.get_token(driver)

data =[]
for phone in phone_list:
    shop_user_no, user_no = osio.get_user_data(phone, token)
    visit_count, oticket = osio.get_user_summary(user_no, shop_user_no, token)
    last_entry = osio.get_user_log(shop_user_no, token)
    data.append([phone, visit_count, oticket, last_entry])
columns = ['phone', 'visit', 'oticket', 'entry']
df = pd.DataFrame(data, columns=columns)
print(df)

no_visit = df.loc[(df['visit'] == '0') & (df['oticket'] == '0')]
print(no_visit)
no_visit_list = no_visit.values.tolist()

user_input = input("\nDelete user (y/n)")
if user_input == "y":
    for val in no_visit_list:
        print(val[0])
        osio.delete_user(driver, val[0])
else:
    print("Programe closed.")

driver.quit()
if os.name != 'nt':
    display.stop()