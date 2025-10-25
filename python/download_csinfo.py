#!/usr/bin/env python3

from pyvirtualdisplay import Display
from datetime import datetime
import osio
import os

if __name__ == "__main__":
    
    print('\n', datetime.now())
    if os.name != 'nt':
        display = Display(visible=0, size=(1920,1080))
        display.start()

    driver = osio.get_driver()
    username, password = osio.get_credential()
    osio.enter_login(driver, username, password)

    osio.download_csinfo(driver)
    print('DOWNDLOAD_CSINFO IS OK.')
    
    driver.quit()
    if os.name != 'nt':
        display.stop()
    print(datetime.now())
