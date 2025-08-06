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
    file_name = "len_20250803_점핑몬스터 미사점_고객정보.xlsx"
    file_path = log_dir + file_name
    # df = pd.read_excel(file_path, dtype = 'str')
    df = pd.read_excel(file_path, dtype = 'str', nrows = 10)

    ls_phone = df['전화번호'].values.tolist()
    ls_visit = list()
    i = 1

    for phone in ls_phone:
        print(f"{i}/{len(ls_phone)} {phone}")
        shop_user_no, user_no = osio.get_sid_uid(phone, token)
        ls_visit.append(osio.get_lastvisit(shop_user_no, token))
        rtime = random.randrange(5,10)
        print(rtime)
        time.sleep(rtime)
        i += 1


    df['마지막방문'] = pd.DataFrame(ls_visit, columns=['마지막방문'])

    df.to_excel("visit_" + file_name, engine='openpyxl')

    driver.quit()
    if os.name != 'nt':
        display.stop()
