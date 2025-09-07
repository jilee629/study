#!/usr/bin/env python3

from pyvirtualdisplay import Display
import osio
import os


osio.print_datetime()
if os.name != 'nt':
    display = Display(visible=0, size=(1920,1080))
    display.start()

driver = osio.get_driver()
username, password = osio.get_credential()
osio.enter_login(driver, username, password)

osio.get_count(driver)
osio.exit_user(driver)
osio.get_count(driver)

driver.quit()
if os.name != 'nt':
    display.stop()
osio.print_datetime()