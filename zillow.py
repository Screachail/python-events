import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/88.0.4324.182 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(
    "https://www.zillow.com/new-york-ny/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A"
    "%7B%22west%22%3A-74.24129293847655%2C%22east%22%3A-73.70158956933592%2C%22south%22%3A40.55923170996765%2C"
    "%22north%22%3A40.84709224733113%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6"
    "%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22"
    "%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C"
    "%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22"
    "%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22min%22%3A200%2C%22max%22%3A1600%7D%2C"
    "%22price%22%3A%7B%22min%22%3A40347%2C%22max%22%3A322776%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22baths%22%3A"
    "%7B%22min%22%3A1%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%7D%2C"
    "%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D",
    headers=header)

data = response.text


soup = BeautifulSoup(data, "html.parser")
all_link_elements = soup.select(".property-card-link")

all_links = []
for link in all_link_elements:
    href = link["href"]
    print(href)
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

all_address_elements = soup.select("address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]

all_price_elements = soup.select('span[data-test="property-card-price"]')
all_prices = []
for tag in all_price_elements:
    text = tag.text.strip()
    price = re.findall('\$\d+(?:,\d+)?', text)[0]
    all_prices.append(price)

print(all_prices)
print(all_addresses)
print(all_links)
# Create Spreadsheet using Google Form
# Substitute your own path here 👇
s = Service("C:/Users/kacper.szafraniec/Downloads/chromedriver_win32/chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, service=s)

for n in range(len(all_prices)):
    # Substitute your own Google Form URL here 👇
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfmho9uUjIOQavf6A_h3Xdo0MfzOLB3QiuIM0J_9sjOvRtUnQ/"
               "viewform?usp=sf_link")

    time.sleep(5)
    address = driver.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div['
                                  '1]/input')
    price = driver.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()