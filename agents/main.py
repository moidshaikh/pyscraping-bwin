import requests
from bs4 import BeautifulSoup
import json

url = "https://deviceatlas.com/blog/list-of-user-agent-strings"
r = requests.get(url)

if not r.ok:
    print("Exiting.")

soup = BeautifulSoup(r.text, "html.parser")

agent_data = {}
tables = soup.select(".table.table-striped")

for el in tables:
    agent_name = el.tr.th.text
    agent_text = el.td.text
    agent_data[agent_name] = agent_text

with open("agent_data.json", "w") as f:
    json.dump(agent_data, f, ensure_ascii=False, indent=4)

print("file written")
