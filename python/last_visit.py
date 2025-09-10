#!/usr/bin/env python3

from pyvirtualdisplay import Display
import osio
import os
import pandas as pd
import time
import random

if __name__ == "__main__":

    if os.name != 'nt':
        display = Display(visible=0, size=(1280, 1024))
        display.start()

    driver = osio.get_driver()

    username, password = osio.get_credential()
    osio.enter_login(driver, username, password)

    token = osio.get_token(driver)
    print(f"-> Token: {token}")

    log_dir = "/home/ubuntu/log/"
    file_name = "len_20250806_점핑몬스터 미사점_고객정보.xlsx"
    file_path = log_dir + file_name
    df = pd.read_excel(file_path, dtype = 'str')
    # df = pd.read_excel(file_path, dtype = 'str', nrows = 10)

    phone_list = df['전화번호'].values.tolist()
    visit_list = []
    entry_list = []
    i = 1

    for phone in phone_list:
        print(f"-> {i}/{len(phone_list)} {phone}")
        
        shop_user_no, user_no = osio.get_user_data(phone, token)
        visit_count = osio.get_user_summary(user_no, shop_user_no, token)[0]
        visit_list.append(visit_count)
        
        last_entry = osio.get_user_log(shop_user_no, token)
        entry_list.append(last_entry)
        
        rtime = random.randrange(10,15)
        print(f"{last_entry} {visit_count} {rtime}")
        time.sleep(rtime)
        i += 1

    df['방문회수'] = visit_list
    df['마지막방문'] = entry_list

    df.to_excel("visit_" + file_name, engine='openpyxl')

    driver.quit()
    if os.name != 'nt':
        display.stop()
