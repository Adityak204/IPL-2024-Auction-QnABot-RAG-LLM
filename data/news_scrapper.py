import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import re

################################################################################################
# IndianExpress
url = "https://indianexpress.com/article/sports/cricket/ipl-auction-2024-live-updates-team-players-list-dubai-9073589/"
response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

# Find all the div elements of class name body-lvblg”
rev_div = soup.findAll("div", attrs={"class", "lvblg-box"})

ie_live_updates = {}
for h in tqdm(range(len(rev_div))):
    try:
        para_list = []
        for p in rev_div[h].findAll("p"):
            para_list.append(p.text.strip())
        ie_live_updates[rev_div[h].find("h2").text.strip()] = para_list
    except Exception as e:
        pass


################################################################################################
# Forbes
url = "https://www.forbesindia.com/article/news/ipl-2024-auction-highlights-the-costliest-purchases-and-how-the-teams-stack-up/90427/1"
response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

# Find all the div elements of class name body-lvblg”
rev_div = soup.findAll("div", attrs={"class", "artical-main-sec MT20 spacediv"})
forbes_story = rev_div[0].text.strip()

################################################################################################
# Live Mint
url = "https://www.livemint.com/sports/cricket-news/ipl-auction-2024-live-updates-india-premier-league-teams-list-19-dec-2023-csk-mi-rcb-srh-kkr-pbks-lsg-gt-srh-rr-players-11702954586192.html#:~:text=IPL%20Auction%202024%20Live%20Updates%3A%20Mitchel%20Starc%20was%20bought%20by,RCB%20for%20%E2%82%B911.50%20crore"
response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

rev_div = soup.findAll("div", attrs={"class": re.compile(r"liveSec live.*")})
mint_live_updates = {}
for h in tqdm(range(len(rev_div))):
    try:
        para_list = []
        for p in rev_div[h].findAll("p"):
            para_list.append(p.text.strip())
        mint_live_updates[rev_div[h].find("h2").text] = para_list
    except Exception as e:
        pass

################################################################################################
# Y20
url = "https://y20india.in/ipl-2024-most-expensive-players/"
response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

rev_div = soup.findAll("p")
y20_news = []
for p in rev_div:
    if len(p.text) > 100:
        y20_news.append(p.text.strip())

################################################################################################
# IE - Team Review
url = "https://indianexpress.com/article/sports/ipl/ipl-2024-squad-analysis-9226554/"
response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

rev_div = soup.findAll("p")
ie_team_review = []
for p in rev_div:
    if len(p.text) > 100:
        ie_team_review.append(p.text.strip())

################################################################################################
# Mint Lounge
url = "https://lifestyle.livemint.com/news/big-story/ipl-2024-indian-premier-league-t20-rishabh-pant-dhoni-111711006659958.html"
response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

story_block = soup.find("div", attrs={"class", "storyContent"})
# print(f"Length of story block = {len(story_block)}")
# story_block = story_block[0]
player_to_look_for = []
for p in story_block.findAll("p"):
    if len(p.text) > 100:
        player_to_look_for.append(p.text.strip())


################################################################################################
# First Post
url = "https://www.firstpost.com/firstcricket/sports-news/ipl-2024-auction-explaining-biggest-trades-and-releases-ahead-of-mini-auction-13440192.html"
response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

rev_div = soup.findAll("p")
biggest_trades = []
for p in rev_div:
    if len(p.text) > 100:
        biggest_trades.append(p.text.strip())


################################################################################################
url = "https://sportstar.thehindu.com/magazine/ipl-2024-auction-review-trends-analysis-squads-best-buys-teams-who-got-it-right-talking-points-money/article67665112.ece"

response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

rev_div = soup.findAll("p")
best_buys = []
for p in rev_div:
    if len(p.text) > 100:
        best_buys.append(p.text.strip())

################################################################################################
# ESPNInfo
url = "https://www.espncricinfo.com/live-blog/ipl-2024-auction-as-it-happened-1413398"
response = requests.get(url)
# Create a soup object and parse the HTML page
soup = bs(response.content, "html.parser")

# Find all the article elements of class name ds-border-line ds-p-6 ds-border-b”
rev_div = soup.findAll("article", attrs={"class", "ds-border-line ds-p-6 ds-border-b"})

espn_as_it_happens = {}
for h in tqdm(range(len(rev_div))):
    try:
        para_list = []
        for p in rev_div[h].findAll(
            "div",
            attrs={
                "class",
                "ds-text-comfortable-m ds-mb-6 ds-text-typo-mid2 ci-live-blog",
            },
        ):
            para_list.append(p.text.strip())
        espn_as_it_happens[rev_div[h].find("h2").text.strip()] = para_list
    except Exception as e:
        pass
