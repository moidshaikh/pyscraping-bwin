from logger import getLogger
from scraper import BwinScraper
import time
lgr = getLogger(__name__)


def main():
    t1_start = time.perf_counter()
    lgr.info("Script start")
    link = "https://sports.bwin.com/cds-api/bettingoffer/fixtures?x-bwin-accessid=NTZiMjk3OGMtNjU5Mi00NjA5LWI2MWItZmU4MDRhN2QxZmEz&lang=en&country=SG&userCountry=SG&fixtureTypes=Standard&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other&sportIds=5&tournamentIds=&competitionIds=&conferenceIds=&isPriceBoost=false&skip=0&take=500&sortBy=Tags"
    b = BwinScraper(link)
    b.fetch_data()
    b.export_raw_json("./output/raw.json")
    b.process_fixtures()
    b.export_json("./output/final.json")
    b.export_csv("./output/final.csv")
    lgr.info(f"Time taken: {time.perf_counter() - t1_start} seconds")
    lgr.info(f"Skipped results(Invalid or Live): {len(b.skipped)}")



def profile_and_run():
    """Profiles the script while running and generates output in `performance.prof` file.
    """
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        main() 
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename="scraper.prof")
    lgr.info("Generated run profile in `performance.prof`")

if __name__ == "__main__":
    main()
    # profile_and_run()
