from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

s=Service("C:/Users/kacper.szafraniec/Downloads/chromedriver_win32.exe")
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options, service=s)
url="https://en.wikipedia.org/wiki/Main_Page"
browser.get(url)

article_number = browser.find_element(By.XPATH, '//*[@id="articlecount"]/a[1]')
print(f"On the Wikipedia there are {article_number.text} articles.")
