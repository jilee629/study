from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



if __name__ == "__main__":

    DRIVER_PATH = '/usr/bin/chromedriver'
    BROWSER_PATH = '/usr/bin/chromium-browser'

    options = Options()
    options.binary_location = BROWSER_PATH
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=DRIVER_PATH)
    
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.google.com")
    print(f"현재 페이지 제목: {driver.title}")
    print(driver.page_source[:200])

    driver.quit()
