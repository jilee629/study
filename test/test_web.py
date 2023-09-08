def sep(num):
    print(f"test({str(num)}) {'-' * 40}")

def test_request():
    import requests
    res = requests.get("https://www.google.com")

    sep(1)
    print(res)
    
    sep(2)
    # http status code: 200(OK), 4XX(Client error responses)
    print(res.status_code)
    # status code가 200 이 아니면 error 발생하도록
    print(res.raise_for_status())

    sep(3)
    print(res.headers)

    sep(4)
    print(res.headers['Content-Type'])

def test_seleinum_dirver():
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--start-maximized")
    # options.add_argument("headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.google.com/')

    return driver

def test_bs_select():
    from bs4 import BeautifulSoup
   
    driver = test_seleinum_dirver()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.quit()
        
    sep(1)
    print(type(driver))
    # <class 'selenium.webdriver.chrome.webdriver.WebDriver'>
    print(type(html))
    # <class 'str'>
    print(type(soup))
    # <class 'bs4.BeautifulSoup'>
        
    sep(2)
    # class는 .으로 시작, 공백은 .으로 처리
    print(soup.select('.uU7dJb'))
    
    sep(3)
    print(soup.select_one('.uU7dJb').text)

    sep(4)
    # class와 a tag의 href 속성 지정
    print(soup.select('.KxwPGc.iTjxkf a[href="https://policies.google.com/privacy?hl=ko&fg=1"]'))
    
    sep(5)
    print(soup.select_one('.KxwPGc.iTjxkf a[href="https://policies.google.com/privacy?hl=ko&fg=1"]').text)
    

def test_selenium_find():
    from selenium.webdriver.common.by import By
    
    driver = test_seleinum_dirver()
   
    sep(1)
    print(driver.find_element(By.CSS_SELECTOR, '.uU7dJb'))
    
    sep(2)
    print(driver.find_element(By.CSS_SELECTOR, '.uU7dJb').text)
    
    sep(3)
    print(driver.find_element(By.CSS_SELECTOR, '.KxwPGc.iTjxkf a[href="https://policies.google.com/privacy?hl=ko&fg=1"]'))
    
    sep(4)
    print(driver.find_element(By.CSS_SELECTOR, '.KxwPGc.iTjxkf a[href="https://policies.google.com/privacy?hl=ko&fg=1"]').text)
    
    driver.quit()


if __name__ == "__main__":
    
    import sys
    
    test = getattr(sys.modules[__name__], sys.argv[1])
    test()