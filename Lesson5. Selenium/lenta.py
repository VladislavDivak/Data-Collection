from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
# chrome_options.add_argument("--windows-size=1920,1080")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe', options=chrome_options)
driver.get('https://lenta.com/promo/')

button = driver.find_element(By.CLASS_NAME, "cookie-usage-notice__button-inner--desktop")
button.click()

driver.implicitly_wait(10)

pages = 0
while pages < 5:
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable(
        (
            By.CLASS_NAME, 'catalog-grid__pagination-button'
        )
    ))
    # button = driver.find_element(By.CLASS_NAME, "catalog-grid__pagination-button")
    button.click()
    pages +=1

items = driver.find_elements(By.CLASS_NAME, 'sku-card-small-container')
for item in items:
    name = item.find_element(By.CLASS_NAME, 'sku-card-small-header__title').text
    rub = item.find_element(By.CLASS_NAME, 'price-label__integer').text
    cop = item.find_element(By.CLASS_NAME, 'price-label__fraction').text
    price = float("".join(rub.split()) + '.'+cop)
    print(name, price)


print()
driver.quit()