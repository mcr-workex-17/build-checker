from bs4 import BeautifulSoup
import requests
import json

build_name = []
status = []
timestamp = []

with open("config.json", "r") as f:
    config = json.load(f)
page = requests.get(config["serverurl"]).text
soup = BeautifulSoup(page, "lxml")
table = soup.find('table', {"id": "projectstatus"}).find_all("tr")[1::]
#fetches the data from a table from the sever specifyed in the config file
for n in table:
    build_name.append(str(n.find("a", {"class": "model-link inside"}).text))
    status.append(str(n.find("img").get('alt', '')))
    timestamp.append(str(n.find_all("td")[2].get('data','')))


build_data = [build_name, status, timestamp]
with open("last_build_data_log.json", "w") as f:
    json.dump(build_data, f)
