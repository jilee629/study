from pyvirtualdisplay import Display
from datetime import datetime, timedelta
import osio
import os, random, time
import pandas as pd

if __name__ == "__main__":

    log_dir = os.path.dirname(__file__) + '/../../log/'
    yesterday = datetime.now() - timedelta(days=1)
    file_name = yesterday.strftime('%Y%m%d') + '_점핑몬스터 미사점_고객정보.xlsx'
    file_path = log_dir + file_name
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
    
    data =[]
    for phone in phone_list:
        shop_user_no, user_no = osio.get_user_data(phone, token)
        visit_count, oticket = osio.get_user_summary(user_no, shop_user_no, token)
        last_entry = osio.get_user_log(shop_user_no, token)
        data.append([phone, visit_count, oticket, last_entry])
        if last_entry is None:
            print(phone, visit_count, oticket, last_entry)
        time.sleep(30)

    columns = ['phone', 'visit', 'oticket', 'entry']
    df = pd.DataFrame(data, columns=columns)
    new_file = log_dir + "unkown_" + file_name
    df.to_excel(new_file, engine='openpyxl')
    
    # pd.set_option('display.max_rows', None)
    # print(df)

    driver.quit()
    if os.name != 'nt':
        display.stop()
