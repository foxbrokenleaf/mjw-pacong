from selenium import webdriver
from selenium.webdriver.common.by import By
import time
brower = webdriver.Chrome()
brower.get("https://www.mjwu.cc/play/1268-1-10/")
time.sleep(10)
value = brower.find_element(By.CLASS_NAME,"conch-hasone conch-adjust-fix")
print(value.text)

