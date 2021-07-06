from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
# from dotenv import load_dotenv

# load_dotenv() 

# ACCESS_KEY = os.getenv('ACCESS_KEY')

driver =  webdriver.Chrome()
driver.maximize_window()
action = ActionChains(driver)

driver.get('https://www.browserstack.com/')

sign_in_btn = '//*[@id="primary-menu"]/li[5]/a'

driver.find_element_by_xpath(sign_in_btn).click()

email_box = 'user_email_login'
driver.find_element_by_id(email_box).send_keys("princeton.b+demo@browserstack.com")

action.send_keys(Keys.TAB).send_keys('Princeton@99').perform()

submit_btn = 'user_submit'
driver.find_element_by_id(submit_btn).click()


# if str(driver.current_url).startswith('https://live.browserstack.com/'):
#     pass
# else:
#     try:
#         live_id = 'live_cross_product_explore'
#         driver.find_element_by_id(live_id).click()
#     except:
#         live_path = '//*[@id="header"]/header/div/div/div/nav/ul/li[1]/a'
#         driver.find_element_by_xpath(live_path).click()

WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "skip-local-installation"))
    ).click()

print("Pressing Windows 10")
windows10 = '//*[@id="os-listing-react"]/div/div[4]/div[2]/div[1]/div/div'
driver.find_element_by_xpath(windows10).click()

print("Pressing Chrome")
xpath_chrome = '//*[@id="desktop-list-react"]/div/div[2]/div[4]/div[1]/div[4]/div/div'
WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_chrome))
    ).click()

print("waiting to load")
new_path = '//*[@id="flashParent"]/object'
element = WebDriverWait(driver, 20).until(
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
element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, id))
    )

action.key_down(Keys.CONTROL).send_keys('L').key_up(Keys.CONTROL).perform()

# action.send_keys(Keys.COMMAND, 'L').perform()
# action_chains.move_to_element_with_offset(elem, 660, 420).perform()
# .send_keys("https://www.google.com/search?q=browerstack")\
# .send_keys(Keys.ENTER)
# action.perform()


print("DONE")

time.sleep(5)
driver.quit()

