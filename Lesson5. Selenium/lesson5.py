from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import pymongo
import time
import math

chrome_options = Options()
# chrome_options.add_argument("--windows-size=1920,1080")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome('./chromedriver/chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/')

#Enter the username and password
username = 'gb_students_787@mail.ru'
password = 'Gfhjkmlkzcneltynjd001#'

button = driver.find_element(By.CLASS_NAME, 'resplash-btn_primary')
button.click()

link = driver.find_elements(By.TAG_NAME, 'iframe')[3].get_attribute('src')
driver.get(link)

user = driver.find_element(By.NAME, 'username')
user.send_keys(username)
button = driver.find_element(By.TAG_NAME,'button')
button.click()
driver.implicitly_wait(5)
login = driver.find_element(By.NAME, 'password')
login.send_keys(password)
button = driver.find_element(By.TAG_NAME,'button')
button.click()

#E-mails storage
mail_list = set()

#Function to collect the e-mails info
def collect_emails(collection_list, total_letters, main_tab):
    for i in range(math.ceil(total_letters/25)+1):
        main_window = driver.window_handles[main_tab]
        driver.implicitly_wait(10)
        letters = driver.find_elements(By.CLASS_NAME, 'llc')

        for letter in letters:
            mail_info = {}
            driver.implicitly_wait(10)
            mail_info['sender'] = letter.find_element(By.CLASS_NAME, 'll-crpt').get_attribute('title')
            mail_info['title'] = letter.find_element(By.CLASS_NAME, 'll-sj__normal').text
            mail_info['datetime'] = letter.find_element(By.CLASS_NAME, 'llc__item_date').get_attribute('title')
            link = letter.get_attribute('href')
            try:
                driver.execute_script("window.open('"+link+"');")
                driver.implicitly_wait(10)
                next_window = driver.window_handles[main_tab+1]
                driver.switch_to.window(next_window)
                try:
                    mail_info['text'] = driver.find_elements(By.TAG_NAME, 'tbody')[1].text
                except:
                    mail_info['text'] = driver.find_element(By.CLASS_NAME, 'gmail_quote_mr_css_attr').text
                driver.close()
                driver.switch_to.window(main_window)
            except:
                mail_info['text'] = None
            collection_list.add(mail_info)
        actions = ActionChains(driver)
        actions.move_to_element(letters[-1])
        actions.perform()

let_sum = float(driver.find_element(By.CLASS_NAME, 'nav__item_child-level_0').get_attribute('title').split(' ')[1])
tab = 0
collect_emails(mail_list, let_sum, tab)

#Collect the mails from other folders, if exists
try:
    folders = driver.find_elements(By.CLASS_NAME, 'nav__item_child-level_1')
    for folder in folders:
        try:
            num_of_let = float(folder.get_attribute('title').split(' ')[1])
            path = folder.get_attribute('href')
            driver.execute_script("window.open('" + path + "');")
            driver.implicitly_wait(10)
            driver.switch_to.window(driver.window_handles[1])
            collect_emails(mail_list, num_of_let, 1)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
except:
    pass

###Creating the database
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['db_letters']
letters = db.letters

unique_mail_list = []
for mail in mail_list:
    if mail not in unique_mail_list:
        unique_mail_list.append(mail)

for m in unique_mail_list:
    try:
        letters.insert_one(m)
    except:
        pass

letters_to_show = pd.DataFrame(list(letters.find()))

driver.quit()