def sep(num):
    print(f"test({str(num)}) {'-' * 40}")


def test_request():
    import requests
    res = requests.get("https://jsonplaceholder.typicode.com/users/1")

    sep(1)
    print(res)
    
    sep(2)
    # http status code: 200(OK), 4XX(Client error responses)
    print(res.status_code)
    # status code가 200 이 아니면 error 발생하도록
    print(res.raise_for_status())

    sep(3)
    print(res.content)

    sep(4)
    print(res.headers)

    sep(5)
    print(res.headers['Content-Type'])

def test_bs_select():
    from bs4 import BeautifulSoup

    html = '<div class="in_wrap place-at-center">\
                <div class="ui-input-text">\
                    <input name="id" placeholder="아이디" value>\
                    <input name="pw" type="password" placeholder="비밀번호" value>\
                </div>\
                <div class="ui-large-button">\
                    <button class="sc-bdVaJa djlRTQ BU2 border">로그인</button>\
                </div>\
            </div>'
    soup = BeautifulSoup(html, 'html.parser')

    sep(1)
    # class는 .으로 시작, 공백은 .으로 처리
    print(soup.select('.sc-bdVaJa.djlRTQ.BU2.border'))

    sep(2)
    # class와 속성 지정
    print(soup.select('.ui-input-text input[name="id"]'))

    sep(3)
    # 바로 아래 단계별로 검색
    print(soup.select('.ui-input-text > button'))

    sep(4)
    # 문자열만 가져오기
    print(soup.select_one('.ui-large-button').text)

def test_selenium_op():
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By

    options = Options()
    # 셀레니움 실행동안 브라우저 닫지 않기
    options.add_experimental_option('detach', True)
    # 개발도구 로그 보지 않기
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--start-maximized")
    # options.add_argument("headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.google.com/')
    data = driver.find_element(By.CSS_SELECTOR, '.MV3Tnb').text
    print(f'결과 : {data}')
    # driver.quit()


if __name__ == "__main__":
    import sys
    test = getattr(sys.modules[__name__], sys.argv[1])
    test()