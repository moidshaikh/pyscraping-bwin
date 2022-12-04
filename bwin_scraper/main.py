from logger import getLogger
from new_scraper import BwinScraper
from pathlib import Path
from time import perf_counter
import asyncio

lgr = getLogger(__name__)

async def process(b):
    b.fetch_data()
    # b.export_raw_json("./output/raw.json")
    # b.process_fixtures()
    # b.export_json("./output/final.json")
    # b.export_csv("./output/final.csv")


def main():
    t1_start = perf_counter()
    lgr.info("Script start")
    link = "https://sports.bwin.com/cds-api/bettingoffer/fixtures?x-bwin-accessid=NTZiMjk3OGMtNjU5Mi00NjA5LWI2MWItZmU4MDRhN2QxZmEz&lang=en&country=SG&userCountry=SG&fixtureTypes=Standard&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other&sportIds=5&tournamentIds=&competitionIds=&conferenceIds=&isPriceBoost=false&skip=0&take=500&sortBy=Tags"
    b = BwinScraper(link)
    asyncio.run(process(b))
    lgr.info(f"Time taken: {perf_counter() - t1_start}")
    lgr.info("fin.")


if __name__ == "__main__":
    main()
    # import cProfile
    # import pstats

    # with cProfile.Profile() as pr:
    #     main() 
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # # stats.print_stats()
    # stats.dump_stats(filename="first.prof")
