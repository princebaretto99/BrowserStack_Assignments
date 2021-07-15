from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browserstack.local import Local
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os
from dotenv import load_dotenv

load_dotenv() 


username = os.getenv("BROWSERSTACK_USERNAME") 
access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
build_name = os.getenv("BROWSERSTACK_BUILD_NAME")
build = os.getenv("BROWSERSTACK_BUILD")
local = os.getenv("BROWSERSTACK_LOCAL")
local_id = os.getenv("BROWSERSTACK_LOCAL_IDENTIFIER")

desired_cap = {
    "os" : "Windows",
    "os_version" : "10",
    "browser" : "Chrome",
    "browser_version" : "latest",
    "projectName" : "Local_testing",
    'name': build_name, # test name
    'build': build,
    'browserstack.local' : local,
    'browserstack.localIdentifier' : local_id
}

normal_cap = {
    "os" : "Windows",
    "os_version" : "10",
    "browser" : "Chrome",
    "browser_version" : "latest",
    "projectName" : "Normal_testing",
    'name': build_name, # test name
    'build': build,
    "browserstack.networkLogs" : "true",
    "browserstack.console" : "verbose",
    "browserstack.geoLocation" : "AR", #ARGENTINA
}
good_mobile_cap = {
    'browserName': 'iPhone',
    'device': 'iPhone 11',
    'realMobile': 'true',
    'os_version': '14.0',
    "browserstack.networkLogs" : "true",
    "projectName" : "Mobile Runs",
    "browserstack.networkProfile" : "4g-lte-good",
    'name': build_name, # test name
    'build': build,
    "browserstack.appiumLogs" : "false"
}

custom_mobile_cap = {
    'browserName': 'iPhone',
    'device': 'iPhone 11',
    'realMobile': 'true',
    'os_version': '14.0',
    "browserstack.debug" : "true",
    "browserstack.networkLogs" : "true",
    "projectName" : "Mobile Runs",
    "browserstack.customNetwork" : "1000,1000,100,1",
    'name': build_name, # test name
    'build': build
}

def run_mobile(mobile_cap):
    driver = webdriver.Remote(
        command_executor='https://'+username+':'+access_key+'@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=mobile_cap)
    try:
        driver.get("https://www.google.com/search?q=Browserstack")
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Loaded"}}')
    except:
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Didnt Load"}}')

    driver.quit()

def run_local(desired_cap):
    # creates an instance of Local
    try:
        bs_local = Local()

        bs_local_args = { "key": access_key , "localIdentifier": local_id}

        #starts the Local instance with the required arguments
        bs_local.start(**bs_local_args)

        print(bs_local.isRunning())

        driver = webdriver.Remote(
            command_executor='https://'+username+':'+access_key+'@hub-cloud.browserstack.com/wd/hub',
            desired_capabilities=desired_cap)

        driver.get("http://localhost:8000/")


        if(str(driver.title).startswith("D")):
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Loaded Locally"}}')
        else:
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Didnt get the Link"}}')

    #stop the Local instance
    except Exception as e:
        print(e)
    finally:
        bs_local.stop()
        driver.quit()

def run_normal(normal_cap):
    driver = webdriver.Remote(
        command_executor='https://'+username+':'+access_key+'@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=normal_cap)
    try:
        driver.get("https://www.google.com/search?q=Browserstack")

        if(driver.title == "Browserstack - Google Search"):
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Loaded"}}')
        else:
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Didnt Load"}}')
    except:
        print("Didnt work!")
    driver.quit()

#python3 LocalTesting.py mobile-good
#python3 LocalTesting.py mobile-custom
#python3 LocalTesting.py local
#python3 LocalTesting.py normal

if sys.argv[1] == "local":
    print("Running Local Testing")
    run_local(desired_cap)
elif sys.argv[1] == "mobile-good":
    print("Mobile Good Running")
    run_mobile(good_mobile_cap)
elif sys.argv[1] == "mobile-custom":
    print("Mobile Custom Running")
    run_mobile(custom_mobile_cap)
elif sys.argv[1] == "normal":
    print("Normal Desktop Running")
    run_normal(normal_cap)    
else:
    print("Invalid Argument")