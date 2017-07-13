import json
import requests
from bs4 import BeautifulSoup
import time
#creates a function called send_slack that sends to slack
def send_slack():
    #opens a config file that contains the channels bots URL and the channel itself
    with open("channels.txt", "r") as f:
        url = json.load(f)
    #opens up a new config file that gives the bot name and instructions of where to send to and where to get the data from
    with open("config.json", "r") as f:
        config = json.load(f)
    bot_name = config["botname"]
    place = config["channel"]
    page = requests.get(config["serverurl"]).text
    soup = BeautifulSoup(page, "lxml")
    table = soup.find('table', {"id": "projectstatus"}).find_all("tr")[1::]
    #fetches the data from a table from the sever specifyed in the config file
    for n in table:
        build_name = "Job Name: " + str(n.find("a", {"class": "model-link inside"}).text)
        status ="Success: " + str(n.find("img").get('alt', ''))
        timestamp = "Timestamp: " + str(n.find_all("td")[2].get('data',''))
        #takes the neccessary data from the the dictionarys (lists for strings) 
        webhook_url = url[place]
        #print url[place] # debugging
        slack_data = {
                "username": " " + bot_name,
                "icon_emoji": ":robot_face:",
                "text": "~~~~~~~~~~~~~~~~~~~~~~\n#*" + place + "* \nBuild =  " + build_name +"\nStatus = " + status + "\nTime =  "  + timestamp + " "
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
#runs the function send_slack
if __name__ == "__main__":
    send_slack()
