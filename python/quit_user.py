#!/usr/bin/env python3

from pyvirtualdisplay import Display
from datetime import datetime
import osio
import os


if __name__ == "__main__":

    if os.name != 'nt':
        display = Display(visible=0, size=(1280, 1024))
        display.start()

    now = datetime.now()
    print("\n", now.strftime("%Y-%m-%d %H:%M:%S %A"))

    driver = osio.get_driver()

    username, password = osio.get_credit()
    osio.enter_login(driver, username, password)
    
    osio.get_count(driver)
    osio.quit_user(driver)
    osio.get_count(driver)
    print('OK')

    driver.quit()
    if os.name != 'nt':
        display.stop()
