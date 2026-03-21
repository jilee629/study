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
    
    year = 2026
    month = 3
    start_date = 20
    end_date = 20
    
    print(year, month, start_date)

    for d in range(start_date, end_date + 1):
        date = str(year) + f"{month:02d}" + f"{d:02d}"
        child_count = osio.get_child_count(date, token)
        print(child_count)
    
    print(year, month, end_date)

    driver.quit()
    if os.name != 'nt':
        display.stop()
