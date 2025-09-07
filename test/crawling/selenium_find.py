driver.find_element(By.NAME, 'search')

driver.find_element(By.CSS_SELECTOR, '.ui-repeat.sc-cSHVUG.keecsQ')
driver.find_element(By.CSS_SELECTOR, '.sc-bMVAic.greGXT button:nth-of-type(2) div strong')
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="아이디를 입력해 주세요."]').send_keys(name)
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

driver.find_element(By.XPATH, '//*[@placeholder="아이디를 입력해 주세요."]')
driver.find_element(By.XPATH, '//*[@type="submit"]')
# // : 문서 전체에서
# * : 모든 요소(Elements)
# @type : type 속성(Attributes)이 "sumit"인 요소를 검색

find_element(By.XPATH, '//[@id="root"]/div[2]/div/div')
# //: 문서 전체에서
# [@id="root"]: id 속성이 "root"인 요소
# /: 현재 요소의 자식 요소를 나타냅니다.

find_element(By.XPATH, '//button[text()="확인"]')
# "확인" 이라는 버튼 요소를 찾고자 할 때

find_element(By.XPATH, '//button[contains(., "확인")]')
# "확인"을 포함하는 버튼 요소를 찾고자 할때

find_element(By.XPATH, '//p[text()="일주일간 보지 않기"]/ancestor::div[3]')
# "일주일간 보지 않기"를 찾고 3번째 상위 div 요소를 찾기

# 대기하기
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]')))
submit_button.click()
