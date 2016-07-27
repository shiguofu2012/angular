from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()
browser.get("https://mp.weixin.qq.com/")
account = browser.find_element_by_name("account").send_keys("shiguofu@hust.edu.cn")
password = browser.find_element_by_id("pwd").send_keys("5082753shi")
time.sleep(2)
browser.find_element_by_id("loginBt").click()
time.sleep(5)
cur = browser.current_url
