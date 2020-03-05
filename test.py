from selenium import webdriver
from time import sleep


driver = webdriver.Ie(r'C:\Users\user\Desktop\IEDriverServer.exe')
sleep(3)
driver.get('https://google.com')
driver.close()
