#!/usr/bin/env python3

from pyvirtualdisplay import Display
from datetime import datetime
import osio
import os

if __name__ == "__main__":

    if os.name != 'nt':
        display = Display(visible=0, size=(1920,1080))
        display.start()

    driver = osio.get_driver()
    username, password = osio.get_credential()
    osio.enter_login(driver, username, password)
    token = osio.get_token(driver)
    
    year = '2025'
    month = '12'
    end_date = 31
    for d in range(1, end_date + 1):
        date = year + month + f"{d:02d}"
        child_count = osio.get_child_count(date, token)
        print(child_count)
    print(date)

    driver.quit()
    if os.name != 'nt':
        display.stop()
