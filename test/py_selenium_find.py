

driver.find_element(By.NAME, 'search')
driver.find_element(By.CSS_SELECTOR, '.ui-repeat.sc-cSHVUG.keecsQ')
driver.find_element(By.CSS_SELECTOR, '.sc-bMVAic.greGXT button:nth-of-type(2) div strong')

driver.find_element(By.CSS_SELECTOR, 'input[placeholder="아이디를 입력해 주세요."]').send_keys(name)
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()


driver.find_element(By.XPATH, '//*[@placeholder="아이디를 입력해 주세요."]')
driver.find_element(By.XPATH, '//*[@type="submit"]')
driver.find_element(By.XPATH, '//button[text()="로그인"]')
driver.find_element(By.XPATH, '//button[contains(., "manager")]')


# 대기하기
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]')))
submit_button.click()
