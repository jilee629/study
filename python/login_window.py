import osio

osio.print_datetime()
driver = osio.get_driver()
username, password = osio.get_credential()
osio.enter_login(driver, username, password)

osio.get_count(driver)

driver.quit()