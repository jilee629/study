from selenium import webdriver

from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from pyvirtualdisplay import Display

def firefox():
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    return driver

if __name__ == "__main__":
    
    display = Display(visible=0, size=(1024, 768))
    display.start()
    
    driver = firefox()