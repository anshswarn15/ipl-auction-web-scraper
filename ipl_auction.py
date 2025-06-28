import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.iplt20.com/auction/2022"
r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")
# print(soup.prettify())

table = soup.find("table", class_="ih-td-tab w-100 auction-tbl")
title = table.find_all("th")

# print(title)
headers = []

for i in title:
    names = i.text.strip() # Added strip() here for robustness
    headers.append(names)

# print(headers)
df = pd.DataFrame(columns=headers)
# print(df)

rows = table.find_all("tr")

# print(rows)

for i in rows[1:]:
    # Find the first td and then the div within it. Handle the case where div is not found.
    first_td_div = i.find_all("td")[0].find("div", class_="ih-pt-cont")
    first_td = first_td_div.text.strip() if first_td_div else ""

    data = i.find_all("td")
    # Exclude the first td as its content (player name) is extracted separately
    row = [tr.text.strip() for tr in data[1:]] # Modified slice to exclude the first element
    row.insert(0,first_td)
    l = len(df)
    df.loc[l] = row

print(df)

df.to_csv("ipl_auction_2022.csv")
