from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
global browser

s=Service("C:/Users/kacper.szafraniec/Downloads/chromedriver_win32.exe")
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options, service=s)
url="https://python.org"
browser.get(url)

dates = browser.find_elements(By.CSS_SELECTOR, ".event-widget time")
events = browser.find_elements(By.CSS_SELECTOR, ".event-widget li a")
events_num = len(dates)
events_dict = {}
for event in range(events_num):
    events_dict[event] = {
        "time": dates[event].text,
        "name": events[event].text,
    }
print(events_dict)

browser.quit()


