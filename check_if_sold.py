import json
from get_data import Item, wait_for_page_load
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time

def load_items_from_json(filename = "list_of_items.json"): 
    with open(filename, 'r') as file: 
        items_dict = json.load(file)
        return [Item(**item) for item in items_dict]
items = load_items_from_json()
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
options = webdriver.FirefoxOptions()
options.set_preference("dom.webnotifications.enabled", False)
#options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver,15, ignored_exceptions= ignored_exceptions)
driver.get("https://www.facebook.com/marketplace/109365765748771/search?availability=in%20stock&daysSinceListed=1&query=electronics&exact=false")
driver.maximize_window()
wait_for_page_load(driver)
email_field = driver.find_element(By.NAME, "email")
password_field = driver.find_element(By.NAME, "pass")
email_field.send_keys("mcneeleyaaron@ymail.com")
password_field.send_keys("Boov50")
password_field.send_keys(Keys.RETURN)
wait.until(EC.invisibility_of_element_located((By.NAME, "email")))

wait_for_page_load(driver)
for item in items: 
    driver.get(item.link)