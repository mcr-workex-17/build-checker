import json
import requests
from bs4 import BeautifulSoup
import time

#get data from log file here:
with open("last_build_data_log.json", "r") as f:
    build_data = json.load(f)

#run the code for each build
for i in range(0, len(build_data[0])):
  #loads slack channel names and corresponding URLs
  with open("channels.txt", "r") as f:
    url = json.load(f)
  #opens up a new config file that gives the bot name and instructions of where to send to and where to get the data from
  with open("config.json", "r") as f:
      config = json.load(f)
  bot_name = config["botname"]
  place = config["channel"]
  #takes the neccessary data from the the dictionarys (lists for strings) 
  webhook_url = url[place]
  #print url[place] # debugging
  slack_data = {
          "username": " " + bot_name,
          "icon_emoji": ":robot_face:",
          "text": "~~~~~~~~~~~~~~~~~~~~~~\n#*" + place + "* \nBuild =  " + build_data[0][i] +"\nStatus = " + build_data[1][i] + "\nTime =  "  + build_data[2][i] + " "
                }
  #this allows python to communicate with slack
  response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
  )
  if response.status_code != 200:
    raise ValueError(
    'Request to slack returned an error %s, the response is:\n%s'
    % (response.status_code, response.text)
  )
