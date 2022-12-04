import requests
import json
from datetime import datetime
import pandas as pd
from logger import getLogger
from typing import List
from concurrent.futures import ThreadPoolExecutor

logr = getLogger(__name__)

class BwinScraper:
    def __init__(self, url: str) -> None:
        """Initializes the scraper.

        Args:
            url (str): URL link of bwin website.
        """
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }
        self.url = url
        self.jsondata = self.fetch_data()
        self.fixture_data = []
        self.skipped = []
        logr.info("Initialized Scraper")

    def fetch_data(self) -> dict:
        """Makes API call to the URL and returns a response. 
           Logs critical if not a valid response.

        Returns:
            dict: returns a dict object from the call
        """
        response = requests.get(
            self.url,
            headers=self.headers,
            proxies={
                "http": "http://paproxy03:Fold-Prevention-See-March-4@gb.smartproxy.com:30000",
            },
        )
        if not response.status_code == 200:
            logr.critical(f"Error while requesting url. Status: {response.status_code}")
            return {}
        logr.info("Requested url.")
        return response.json()

    def export_raw_json(self, outfile="raw_output.json") -> None:
        """Exports raw json response to a file. To test out the results
        Args:
            outfile (str, optional): file name for export file. Defaults to "raw_output.json".
        """
        with open(outfile, "w") as f:
            json.dump(self.jsondata, f, indent=4)
        logr.info(f"Saved raw json response in {outfile}")


    def process_match(self, fi: dict) -> None:
        """Processes each entry in the fixtures dict returned from API call. 
        Match is skipped if it's live.
        There are some matches which are invalid. Player promotions
        Args:
            fi (dict): response entry object in fixture dict.
        """
        datefmt = "%Y-%m-%d %H:%M"
        datefix = lambda x: datetime.strftime(datetime.fromisoformat(x), datefmt)
        if fi["stage"] == "Live":
            logr.info(f"Skipping Live match. {fi['id']}")
            self.skipped.append(fi["id"])
            return 
        f = {}
        try:
            f["tournament"] = fi["tournament"]["name"]["value"]
            f["eventName"] = fi["name"]["value"].replace("-", "vs")
            f["player1"] = fi["participants"][0]["name"]["value"]
            f["player2"] = fi["participants"][1]["name"]["value"]
            f["player1_odds"] = fi["games"][0]["results"][0]["odds"]
            f["player2_odds"] = fi["games"][0]["results"][1]["odds"]
            f["eventdate"] = datefix(fi["startDate"][:-1])
            f["lastupdate"] = datefix(fi["cutOffDate"][:-1])
        except IndexError as e:
            logr.error(f'{e}. Invalid match. id: {fi["id"]}')
            self.skipped.append(fi["id"])
            return
        finally:
            self.fixture_data.append(f)

    def process_fixtures(self) -> None:
        """
            Processes all fixtures we get in response.json()

            Returns: None
        """
        # Fetching all fixtures from response json
        fixtures = self.jsondata["fixtures"]
        # using concurrentcy
        with ThreadPoolExecutor() as executor:
            executor.map(self.process_match, fixtures)
        return None

    def export_csv(self, outfile="fixture_data.csv") -> None:
        """Generate CSV of the required data.

        Args:
            outfile (str, optional): filename of export file. Defaults to "fixture_data.csv".
        """
        df = pd.DataFrame(self.fixture_data)
        df.to_csv(outfile, index=False)
        logr.info("Exported results to {} in same folder.".format(outfile))

    def export_json(self, outfile="fixture_data.json") -> None:
        logr.info(f"{len(self.fixture_data)} total matches.")
        # Skipping invalid matches
        data = [
            x for x in self.fixture_data if "player1" in x.keys()
        ]
        logr.info(f"{len(data)} total matches (excluding live and invalid ).")
        with open(outfile, "w") as f:
            json.dump(data, f, indent=4)
        logr.info(f"Exporting to json file. {outfile}")
