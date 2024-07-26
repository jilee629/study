from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()

service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)

