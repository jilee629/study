#!/usr/bin/env python3

from pyvirtualdisplay import Display
from datetime import datetime
from dateutil.relativedelta import relativedelta
import osio
import os, random, time
import pandas as pd

log_dir = "/home/ubuntu/log"

if __name__ == "__main__":
    
    now = datetime.now()
    yesterday = now - relativedelta(days=1)
    file_name = yesterday.strftime('%Y%m%d') + '_점핑몬스터 미사점_고객정보.xlsx'
    print("FILE :", file_name)
    file_path = os.path.join(log_dir, file_name)
    df = pd.read_excel(file_path, dtype = 'str')
    df_noticket = df.loc[df['오시오 잔여값'].isna()]
    phone_list = random.sample(df_noticket["전화번호"].values.tolist(), 500)

    if os.name != 'nt':
        display = Display(visible=0, size=(1920,1080))
        display.start()

    driver = osio.get_driver()
    username, password = osio.get_credential()
    osio.enter_login(driver, username, password)
    token = osio.get_token(driver)
    
    for i, phone in enumerate(phone_list):
        print(i, end=',', flush=True)

        lenth = len(phone)
        shop_user_no, user_no = osio.get_user_data(phone, token)
        visit_count, oticket = osio.get_user_summary(user_no, shop_user_no, token)
        last_entry = osio.get_user_log(shop_user_no, token)

        entry_date = datetime.fromisoformat(last_entry).replace(tzinfo=None)
        ref_date = now - relativedelta(years=2)
        diff_date = entry_date - ref_date

        user = [lenth, phone, visit_count, oticket, last_entry, diff_date.days]

        if last_entry is None:
            print("\n", user)
        elif diff_date.days < 0:
            print("\n", user)

        time.sleep(30)

    driver.quit()
    if os.name != 'nt':
        display.stop()
