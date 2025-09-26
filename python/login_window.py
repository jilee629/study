from pyvirtualdisplay import Display
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


    phone = "01035917425"
    shop_user_no, user_no = osio.get_user_data(phone, token)
    last_entry = osio.get_user_log(shop_user_no, token)
    print(last_entry)


    # osio.get_count(driver)

    driver.quit()
    if os.name != 'nt':
        display.stop()