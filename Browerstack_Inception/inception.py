from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv() 

ACCESS_KEY = os.getenv('ACCESS_KEY')
PASS = os.getenv('USER_PASS')

caps = [{
"os" : "OS X",
"os_version" : "Catalina",
"browser" : "Edge",
"browser_version" : "latest",
'name': 'Inception-Parallel-Run-1', # test name
 'build': 'Inception Build ',
 'browserstack.use_w3c' : 'true'
},
{
"os" : "OS X",
"os_version" : "Big Sur",
"browser" : "Chrome",
"browser_version" : "latest",
'name': 'Inception-Parallel-Run-2', # test name
 'build': 'Inception Build ',
 'browserstack.use_w3c' : 'true'
},
{
"os" : "OS X",
"os_version" : "Big Sur",
"browser" : "Edge",
"browser_version" : "latest",
'name': 'Inception-Parallel-Run-3', # test name
 'build': 'Inception Build ',
 'browserstack.use_w3c' : 'true'
}]

single_caps = {
"os" : "OS X",
"os_version" : "Big Sur",
"browser" : "Edge",
"browser_version" : "latest",
'name': 'Inception-Parallel-Run-3', # test name
 'build': 'Inception Build ',
 'browserstack.use_w3c' : 'true'
}

def run_session(desired_cap):
    # driver =  webdriver.Chrome()
    driver = webdriver.Remote(
        command_executor='https://princetonbaretto_7D2Tbt:'+ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=desired_cap)

    driver.maximize_window()
    action = ActionChains(driver)
    try:
        driver.get('https://www.browserstack.com/')

        sign_in_btn = '//*[@id="primary-menu"]/li[5]/a'

        driver.find_element_by_xpath(sign_in_btn).click()

        email_box = 'user_email_login'
        driver.find_element_by_id(email_box).send_keys("princeton.b+demo@browserstack.com")

        pass_box = 'user_password'
        driver.find_element_by_id(pass_box).send_keys(PASS)

        submit_btn = 'user_submit'
        driver.find_element_by_id(submit_btn).click()

        time.sleep(5)

        driver.get("https://live.browserstack.com/dashboard")
        try:
            WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "skip-local-installation"))
                ).click()
        except:
            print("No- skip- Local")

        print("Pressing Windows 10")
        windows10 = '//*[@id="os-listing-react"]/div/div[4]/div[2]/div[1]/div/div'
        driver.find_element_by_xpath(windows10).click()

        print("Pressing Chrome")
        xpath_chrome = '//*[@id="desktop-list-react"]/div/div[2]/div[4]/div[1]/div[6]/div/div'
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_chrome))
            ).click()

        print("waiting to load")
        time.sleep(10)

        new_path = '//*[@id="flashParent"]/object'
        element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, new_path))
            )

        print("executing command")

        pathclose = '//*[@id="settings-menu"]/div[2]/div/div[2]/div[4]/div/div[4]/button'
        WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, pathclose))
            ).click()

        try:
            pathsetting = '//*[@id="settings"]/div/label'
            WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, pathsetting))
                ).click()
        except:
            print("Didnt Find")
            pass

        id = 'flashlight-overlay'
        element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, id))
            )
        element.click()

        time.sleep(15)
        print("ACTION")
        if(desired_cap["os"] == 'OS X'):
            action.send_keys(Keys.COMMAND, 'l').perform()
        time.sleep(1)
        action.reset_actions()

        if(desired_cap["os"] == 'Windows'):
            new_action = ActionChains(driver)
            new_action.send_keys("browerstack").send_keys(Keys.ENTER).perform()
        else:
            new_action = ActionChains(driver)
            new_action.send_keys("https://www.google.com/search?q=browerstack").send_keys(Keys.ENTER).perform()

        time.sleep(2)

        print("DONE")

        time.sleep(5)
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Passed!"}}')
    except:
        print("Errorr Occured")
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Failed"}}')
    finally:
        driver.quit()


# run_session(caps)
# run_session(single_caps)
for cap in caps:
    run_session(cap)
# for cap in caps:
#     Thread(target=run_session, args=(cap,)).start()