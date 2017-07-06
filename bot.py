import json
import requests
from bs4 import BeautifulSoup 
import time
def send_slack():
    channels = open("/config/channels.txt", "r")
    channelstxt = channels.readlines()
    url = {}
    for linenumber in range(0,len(channelstxt),2):
        channelname = channelstxt[linenumber].strip()
        channelurl = channelstxt[linenumber+1].strip()
        url[channelname] = channelurl


    config = open("/config/config.txt", "r")
    configtxt = config.readlines()
    bot_name = configtxt[1].strip()
    place = configtxt[3].strip()
    page = requests.get(configtxt[5].strip()).text
    soup = BeautifulSoup(page, "lxml")
    table = soup.find('table', {"id": "projectstatus"}).find_all("tr")[1::]


    for n in table:      
        build_name = "Job Name: " + str(n.find("a", {"class": "model-link inside"}).text)
        status ="Success: " + str(n.find("img").get('alt', ''))
        timestamp = "Timestamp: " + str(n.find_all("td")[2].get('data',''))

        webhook_url = url[place]
        print url[place]
        slack_data = {
                "username": " " + bot_name,
                "icon_emoji": ":robot_face:",
                "text": "#build_announce \nBuild =  " + build_name +"\nStatus = " + status + "\nTime =  "  + timestamp + " "
                        }
        #these allows python to communicate with slack
        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

while __name__ == "__main__":
    send_slack()

