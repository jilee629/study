from pyvirtualdisplay import Display
import osio
import os

if __name__ == "__main__":

    if os.name != 'nt':
        display = Display(visible=0, size=(1920,1080))
        display.start()
    
    osio.print_datetime()
    driver = osio.get_driver()
    username, password = osio.get_credential()
    osio.enter_login(driver, username, password)

    osio.get_count(driver)

    driver.quit()
    if os.name != 'nt':
        display.stop()
