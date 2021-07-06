import time
import os
import sys
from selenium import webdriver
from percy import percy_snapshot
import os


if(os.getenv("PERCY_BRANCH") == "production"):
    baseURL = "https://www.browserstack.com"
    print("PROD")
else:
    baseURL = "https://k8s.bsstag.com"
    print("STAGING")

driver = webdriver.Chrome()

endpoints = {
    "Index Route":"/",
    "Pricing Route":"/pricing",
    "Integration_Automate Route":"/integrations/automate",
    "Docs":"/docs"
    }

for endpoint in endpoints.keys():
    print(baseURL + endpoints[endpoint])
    driver.get(baseURL + endpoints[endpoint])
    percy_snapshot(driver, endpoint)

