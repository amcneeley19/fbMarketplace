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
import json
from bs4 import BeautifulSoup
class Item: 
    def __init__(self, title, price, location, time_on_market, link) -> None:
        self.title = title
        self.price = price 
        self.location = location 
        self.time_on_market = time_on_market
        self.link = link
    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Price: {self.price}\n"
                f"Location: {self.location}\n"
                f"Time on Market: {self.time_on_market}\n"
                f"Link: {self.link}")
    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "location": self.location,
            "time_on_market": self.time_on_market,
            "link": self.link
        }
    def update_price(self, new_price): 
        self.price = new_price
    def update_time_on_market(self, new_time_on_market): 
        self.new_time_on_market = new_time_on_market

def save_items_to_json(items, filename): 
    items_dict = [item.to_dict() for item in items]
    with open(filename, 'w') as file: 
        json.dump(items_dict,file,indent=4)

def wait_for_page_load(driver, timeout=30):
    end_time = time.time()+ timeout
    while time.time() < end_time: 
        ready_state = driver.execute_script("return document.readyState")
        if ready_state == "complete": 
            print("Page has fully loaded.")
            return
        time.sleep(0.5)
    print("Page did not load in {timeout} seconds")
def get_links(xpath, retries = 5): 
    attempt = 0 
    links = []
    while attempt < retries: 
        try: 
            items = driver.find_elements(By.XPATH, xpath)
            for item in items: 
                if "Sponsored" in item.text: 
                    continue
                try:
                    link_element = item.find_element(By.TAG_NAME,"a")
                    href = link_element.get_attribute("href")
                    links.append(href)
                except NoSuchElementException: 
                    print("NO Such Element for" + item.text)
            break
        except StaleElementReferenceException: 
            print(f"StaleElement on {attempt} attempt")
            attempt += 1 

        except TimeoutException:
            print("Timed Out")
            break
    return links
def scroll_down(amount):
    for i in range(amount): 
        driver.execute_script("document.documentElement.scrollIntoView(false);")
        time.sleep(1)
if __name__ == "__main__":

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
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class = 'x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24']")))
    scroll_down(1)
    list_of_items=[]
    wait_for_page_load(driver)
    links = get_links("//div[@class = 'x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24']")
    for link in links: 
        try: 
            driver.get(link)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            title = soup.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x3x7a5m xngnso2 x1qb5hxa x1xlr1w8 xzsf02u')
            price = soup.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 xk50ysn xzsf02u')
            location = soup.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1nxh6w3 x1sibtaa xo1l8bm xi81zsa')
            time_on_market = soup.find('div', class_='x9f619 x1ja2u2z xzpqnlu x1hyvwdk x14bfe9o xjm9jq1 x6ikm8r x10wlt62 x10l6tqk x1i1rx1s')
            #title = driver.find_element(By.XPATH, "//span[@class = 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x3x7a5m xngnso2 x1qb5hxa x1xlr1w8 xzsf02u']")
            #price = driver.find_element(By.XPATH, "//span[@class = 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 xk50ysn xzsf02u']")
            #location = driver.find_element(By.XPATH, "//span[@class = 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1nxh6w3 x1sibtaa xo1l8bm xi81zsa']")
            #time_on_market = driver.find_element(By.XPATH, "//div[@class = 'x9f619 x1ja2u2z xzpqnlu x1hyvwdk x14bfe9o xjm9jq1 x6ikm8r x10wlt62 x10l6tqk x1i1rx1s']")
            if title and price and location and time_on_market:
                new_item = Item(title.text,price.text,location.text,time_on_market.text, link)
                print(new_item.__str__())
                list_of_items.append(new_item)
            wait_for_page_load(driver)
        except TimeoutException:
            print("Timed Out")
        except Exception as e: 
            print(f"Error with {link}: {e}")
    save_items_to_json(list_of_items,"list_of_items.json")