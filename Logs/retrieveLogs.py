import os
from dotenv import load_dotenv
import requests

load_dotenv() 
ACCESS_KEY = os.getenv('BROWSERSTACK_ACCESS_KEY')
USERNAME = os.getenv('BROWSERSTACK_USERNAME')
SESSION_ID = "ca79421cfa151e33eb163f95fac2551cdeee0dfa"

import requests

response = requests.get('https://api.browserstack.com/automate/sessions/'+SESSION_ID+'.json', auth=(USERNAME, ACCESS_KEY))
print("###############################################")
print("Video URL : ")
print(response.json()['automation_session']["video_url"])

print("###############################################")
log_URL = response.json()['automation_session']["logs"]
print("Saving Logs...")
with open("sessionLogs.txt",'w') as f:
    f.write(requests.get(log_URL, auth=(USERNAME, ACCESS_KEY)).text)