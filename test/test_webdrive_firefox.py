from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager


from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

display = Display(visible=0, size=(1024, 768))
display.start()

service = Service(GeckoDriverManager().install())
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Firefox(service=service)



