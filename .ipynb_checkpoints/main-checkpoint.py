import requests
import time

import random
from logger import getLogger

lgr = getLogger("Main")

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
]


u1 = "https://sports.bwin.com/cds-api/offer-grouping/grid-view/all/regional?x-bwin-accessid=NTZiMjk3OGMtNjU5Mi00NjA5LWI2MWItZmU4MDRhN2QxZmEz&lang=en&country=GB&usercountry=GB"
u2 = "https://sports.bwin.com/cds-api/bettingoffer/fixtures?x-bwin-accessid=NTZiMjk3OGMtNjU5Mi00NjA5LWI2MWItZmU4MDRhN2QxZmEz&lang=en&country=SG&userCountry=SG&fixtureTypes=Standard&state=Latest&offerMapping=Filtered&offerCategories=Gridable&fixtureCategories=Gridable,NonGridable,Other&sportIds=5&tournamentIds=&competitionIds=&conferenceIds=&isPriceBoost=false&skip=0&take=50&sortBy=Tags"
s = requests.Session()
s.headers.update({"user-agent": random.choice(user_agent_list)})
url = "https://sports.bwin.com"

r = s.get(url)
lgr.info(r.status_code)
lgr.error(r.headers)


# url = "https://sports.bwin.com/en/api/clientconfig"
# r = s.get(url)
