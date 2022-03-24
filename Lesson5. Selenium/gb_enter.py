from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get('https://gb.ru/login')

elem = driver.find_element(By.ID, 'user_email')
elem.send_keys('gb_students_787@mail.ru')

elem = driver.find_element(By.ID, 'user_password')
elem.send_keys('Gfhjkmlkzcneltynjd001#')

elem.send_keys(Keys.ENTER)

# link = driver.find_element(By.XPATH, "//a[contains(@href, '/users/')]").get_attribute('href')
# driver.get(link)
driver.get('https://gb.ru/profile?tab=info')
gender = driver.find_element(By.NAME, "user[gender]")
select = Select(gender)
select.select_by_value('male')

# gender.submit()
# driver.back()
# driver.forward()
# driver.refresh()
print()

driver.quit()