import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service


browser = webdriver.Edge()
browser.get("http://www.baidu.com")
time.sleep(10000)
