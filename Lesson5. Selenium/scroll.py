from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe', options=chrome_options)
driver.get('https://zen.yandex.ru/')

for i in range(5):
    articles = driver.find_elements(By.TAG_NAME, "article")
    actions = ActionChains(driver)
    actions.move_to_element(articles[-1])
    actions.perform()
    time.sleep(5)



print()
driver.quit()