from selenium import webdriver
from pyvirtualdisplay import Display


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def chrome():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

def chromium():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))


from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def firefox():
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

if __name__ == "__main__":
    
    display = Display(visible=0, size=(1024, 768))
    display.start()
    
    # chrome()
    # chromium()
    firefox()

