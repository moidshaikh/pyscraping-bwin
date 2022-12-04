import requests
import json
from datetime import datetime
import pandas as pd
from logger import getLogger
from typing import List
import asyncio
from aiohttp import ClientSession

logr = getLogger(__name__)


class BwinScraper:
    def __init__(self, url: str) -> None:
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }
        self.url = url
        self.jsondata = self.fetch_data()
        self.fixture_data = []
        logr.info("Initialized Scraper")

    async def fetch_data(self) -> dict:
        with ClientSession() as session:
            with session.get(self.url, headers=self.headers) as response:
                response = response.read()
        # response = requests.get(
        #     self.url,
        #     headers=self.headers,
        #     proxies={
        #         "http": "http://paproxy03:Fold-Prevention-See-March-4@gb.smartproxy.com:30000",
        #         "https": "http://paproxy03:Fold-Prevention-See-March-4@gb.smartproxy.com:30000",
        #     },
        # )
        if not response.status_code == 200:
            logr.critical(f"Error while requesting url. Status: {response.status_code}")
            return {}
        logr.info("Requested url.")
        return response.json()

    async def export_raw_json(self, outfile="raw_output.json") -> None:
        async with open(outfile, "w") as f:
            json.dump(self.jsondata, f, indent=4)
        logr.info(f"Saved raw json response in {outfile}")

    def process_fixture(self, fi: dict) -> None:
        # skipping live matches
        datefmt = "%Y-%m-%d %H:%M"
        datefix = lambda x: datetime.strftime(datetime.fromisoformat(x), datefmt)
        if fi["stage"] == "Live":
            logr.info(f"Skipping Live match. {fi['id']}")
            return {}
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
            logr.error(f'{e}. Invalid match. Failed at id: {fi["id"]}')
            return {}
        finally:
            self.fixture_data.append(f)
        

    async def process_fixtures(self) -> None:
        # Fetching all fixtures from response json
        fixtures = self.jsondata["fixtures"]
        async for fi in fixtures:
            self.process_fixture(fi)
        return 

    async def export_csv(self, outfile="fixture_data.csv") -> None:
        df = pd.DataFrame(self.fixture_data)
        df.to_csv(outfile, index=False)
        logr.info(f"Exported results to {outfile}.")

    async def export_json(self, outfile="fixture_data.json") -> None:
        data = [
            x for x in self.fixture_data if "player1" in x.keys()
        ]  # Skipping promotional matches
        async with open(outfile, "w") as f:
            json.dump(data, f, indent=4)
        logr.info(f"Exporting to json file. {outfile}")
