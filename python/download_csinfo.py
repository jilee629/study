#!/usr/bin/env python3

from pyvirtualdisplay import Display
from datetime import datetime
import osio
import os


if __name__ == "__main__":

    if os.name != 'nt':
        display = Display(visible=0, size=(1024, 768))
        display.start()

    now = datetime.now()
    print("\n", now.strftime("%Y-%m-%d %H:%M:%S %A"))

    driver = osio.get_driver()
    username, password = osio.get_credit()
    osio.enter_login(driver, username, password)
    
    osio.download_csinfo(driver)
    print('OK')

    driver.quit()
    if os.name != 'nt':
        display.stop()

    csfile = now.strftime("%Y%m%d") + "_점핑몬스터 미사점_고객정보.xlsx"
    osio.get_phone_len(csfile)
