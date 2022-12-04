import requests
import json
from datetime import datetime
import pandas as pd
from logger import getLogger


logr = getLogger("scraper")


class BwinScraper:
    def __init__(self, url="") -> None:
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }
        self.url = url
        self.jsondata = self.fetch_data()
        logr.info("Initialized Scraper")

    def fetch_data(self) -> dict:
        response = requests.get(
            self.url,
            headers=self.headers,
        )
        if not response.status_code == 200:
            logr.error(f"Error while requesting url. Status: {response.status_code}")
            return {}
        logr.info("Requested url.")
        return response.json()

    def save_raw_response_json(self) -> None:
        with open("output.json", "w") as f:
            json.dump(self.jsondata, f, indent=4)
        logr.info("Saved raw json response in `output.json`")

    def process_fixtures(self):
        fixtures = self.jsondata["fixtures"]


link = "https://sports.bwin.com/cds-api/bettingoffer/fixtures?x-bwin-accessid=NTZiMjk3OGMtNjU5Mi00NjA5LWI2MWItZmU4MDRhN2QxZmEz&lang=en&country=SG&userCountry=SG&fixtureTypes=Standard&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other&sportIds=5&tournamentIds=&competitionIds=&conferenceIds=&isPriceBoost=false&skip=0&take=500&sortBy=Tags"
b = BwinScraper(link)
print(type(b.fetch_data()))

# # all_fixtures = jsondata["fixtures"]
# fixtures = jsondata["fixtures"]
# datefmt = "%Y-%m-%d %H:%M"
# datefix = lambda x: datetime.strftime(datetime.fromisoformat(x), datefmt)

# for fi in fixtures:
#     if fi['stage'] == "Live":
#         pass
#     tournament = fi["tournament"]['name']['value']
#     eventName = fi["name"]["value"].replace('-','vs')
#     player1 = fi["participants"][0]['name']['value']
#     player2 = fi["participants"][1]['name']['value']
#     player1_odds = fi['games'][0]['results'][0]['odds']
#     player2_odds = fi['games'][0]['results'][1]['odds']
#     eventdate = datefix(fi["startDate"][:-1])
#     lastupdate = datefix(fi["cutOffDate"][:-1])
