from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv() 

username = os.getenv("BROWSERSTACK_USERNAME") 
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
android_app_url = os.getenv("ANDROID_APP_URL")
custom_id = "WikipediaApp"

def run_android():
    desired_caps = {
        "project" : "App-Automate",
        "build": "Python Android",
        "device": "Samsung Galaxy S8 Plus",
        "name" : "Wikipedia App Run",
        "app": custom_id,
        "browserstack.app_version" : "-1"
    }

    driver = webdriver.Remote("https://" + username + ":" + access_key + "@hub-cloud.browserstack.com/wd/hub", desired_caps)

    search_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
    )
    search_element.click()

    search_input = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
    )
    search_input.send_keys("BrowserStack")
    time.sleep(5)

    search_results = driver.find_elements_by_class_name("android.widget.TextView")
    assert(len(search_results) > 0)

    if(len(search_results) > 0):
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Passed!"}}')
    else:
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Failed!"}}')
    driver.quit()

run_android()