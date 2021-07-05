from bs4 import BeautifulSoup
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv() 

ACCESS_KEY = os.getenv('ACCESS_KEY')

caps = [{
 'os_version': '10',
 'resolution': '1920x1080',
 'browser': 'Chrome',
 'browser_version': 'latest',
 'os': 'Windows',
 'name': 'Amazon-Parallel-Run', # test name
 'build': 'Amazon Build Number 1' 
},
{
"os" : "Windows",
"os_version" : "10",
"browser" : "Firefox",
"browser_version" : "latest",
'name': 'Amazon-Parallel-Run', # test name
 'build': 'Amazon Build Number 2'
},
{
"os" : "OS X",
"os_version" : "Big Sur",
"browser" : "Chrome",
"browser_version" : "latest",
'name': 'Amazon-Parallel-Run', # test name
 'build': 'Amazon Build Number 3'
},
{
"os" : "OS X",
"os_version" : "Big Sur",
"browser" : "Firefox",
"browser_version" : "latest",
'name': 'Amazon-Parallel-Run', # test name
 'build': 'Amazon Build Number 4'
},
{
"os" : "Windows",
"os_version" : "10",
"browser" : "Edge",
"browser_version" : "latest",
'name': 'Amazon-Parallel-Run', # test name
 'build': 'Amazon Build Number 5'
}]

def run_session(desired_cap):
    driver = webdriver.Remote(
        command_executor='https://princetonbaretto_7D2Tbt:'+ACCESS_KEY+'@hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=desired_cap)

    #initializing Driver Object
    # driver = webdriver.Chrome()
    driver.maximize_window()
    #Opening the website
    driver.get("https://www.amazon.in")

    #Finding the Search Bar and typing
    elem = driver.find_element_by_id("twotabsearchtextbox")
    elem.send_keys("iPhone X")

    #Hitting the search button
    submit_btn = driver.find_element_by_id("nav-search-submit-button")
    submit_btn.click()

    #Waiting and then sorting by option
    click_path = '/html/body/div[1]/div[2]/span/div/span/h1/div/div[2]/div/div/form/span/span/span/span/span[2]'
    # click_btn = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, click_path))
    #     )
    # click_btn = driver.find_element_by_xpath(click_path)
    click_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "a-autoid-0-announce"))
        )
    click_btn.click()

    #clicking the high to low selection
    id = 's-result-sort-select_2'
    click_btn1 = driver.find_element_by_id(id)
    click_btn1.click()

    #Waiting and Clicking the IOS button
    path_for_IOS = '/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[3]/span/div[1]/span/div/div/div[7]/ul[1]/li[4]/span/a/span'
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, path_for_IOS))
        )
    if(element.is_enabled()):
        element.click()
    else:
        pass
    time.sleep(3)

    #Getting the HTML content
    html_content = driver.page_source
    #Converting raw html into bs4 object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Finding All the product divs
    main_div_all = soup.find_all("div", {"class": "sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"})

    all_data = []
    for divs in main_div_all:
        data = {}
        #Picking each product and removing its details
        try:
            data["Product_Name"] = divs.find("span", {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
            data["Link"] = divs.find("a", {"class" : "a-link-normal a-text-normal"}).get("href")
            data["Product_Price"] = divs.find("span" , {'class': 'a-price-whole'}).text

            all_data.append(data)
        except:
            pass

    # Print the data collected
    print(all_data[0])

    try:
        if len(all_data) != 0:
            # print("Got response")
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Got Data"}}')
    except TimeoutException:
        # print("Failed TEST")
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Didnt get the data"}}')
    finally:
        driver.quit()

for cap in caps:
    Thread(target=run_session, args=(cap,)).start()