import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import re
import pickle

news_articles = []
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

# Appending Indian-express
for k in ie_live_updates:
    if len(ie_live_updates[k]) > 1:
        _string = (
            k.replace("IPL Auction 2024 Live Updates: ", "")
            + "\n"
            + "\n".join(ie_live_updates[k])
        )
    else:
        _string = (
            k.replace("IPL Auction 2024 Live Updates: ", "")
            + "\n"
            + ie_live_updates[k][0]
        )
    news_articles.append(_string)

################################################################################################
# Forbes
forbes = [
    "Australian pacer Mitchell Starc, bought by KKR, was the most expensive player for Rs. 24.75 crore",
    "The recent IPL 2024 auction in Dubai, 72 players were sold to 10 teams for Rs 230.45 crore. Australian pacer Mitchell Starc was the most expensive player, bought by the Kolkata Knight Riders (KKR) for a record Rs. 24.75 crore. Pat Cummins, the skipper of the World Cup-winning Australian team, was the second-costliest player at the auction, being bought by the Sunrisers Hyderabad (SRH) for Rs 20.5 crore.",
    "Daryl Mitchell and Harshal Patel were the third- and fourth-most expensive players that the Chennai Super Kings (CSK) and Punjab Kings (PK) bought for Rs 14 and Rs. 11.75 crore, respectively. Star players like ex-Australian skipper Steve Smith, Josh Hazelwood, Josh Inglis, and Adil Rashid went unsold in the auction. <br/><br/>The purse cap was Rs 100 crore in this IPL. Most of the players were retained by the teams before the auction. KKR spent most in this auction after buying ten players for Rs 31.35 crore. It has retained 15 players at the cost of Rs 67.30 crore, but the team is still two players short and has only Rs 1.35 crore left in its purse. <br/><br/>Sunrisers Hyderabad, which bought six players for Rs 30.80 crore, spent the second-highest. It retained its 19 players before the auction at the cost of Rs 66 crore. The team is still left with Rs 3.20 crore after completing its squad of 25 players.  <br/><br/>The five-time IPL trophy-winning CSK bought New Zealander all-rounder Daryl Mitchell and uncapped youngster Sameer Rizvi for Rs 14 and Rs 8.4 crore, respectively. The team bought a total of six players at Rs 30.40 crore. CSK has retained 19 players, including superstar captain MS Dhoni, Ajinkya Rahane, Ruturaj Gaikwad, Devon Conway, and Mitchell Santner. <br/><br/>Mumbai Indians (MI), which has also won the IPL trophy five times, spent Rs 16.70 crore in the auction for eight players. However, the team bought ex-Gujarat Titans captain Hardik Pandya for a hefty sum of Rs 15 crore weeks before the auction in an all-cash deal. After spending Rs 82.25 crore in retentions, MI is left with Rs 1.05 crore. <br/><br/>Delhi Capitals (DC) has Rs 9.9 crore, the highest among all teams, in its purse despite completing its quota of 25 players. The team spent Rs 19.05 crore on nine players while retaining 16 for Rs 71.05 crore. The costliest purchases for DC are Kumar Kushagra and Jhye Richardson, who were bought for Rs 7.2 crore and Rs 5 crore, respectively. IPL 2024 auction: Five players who can cause a bidding war</a></i></b><br/><br/>Rajasthan Royals has the least amount in its purse after the auction and is still short by three players. The team is left with Rs 20 lakh after spending Rs 14.30 crore on five players, and Rs 85.50 to retain 17 players. The team retained emerging stars like Yashasvi Jaiswal, Riyan Parag, and Navdeep Saini and experienced players like Shimron Hetmyer, Jos Buttler, and Trent Boult. <br/><br/>Royal Challengers Bangalore (RCB), trying to build a team that can get them their first IPL title, spent Rs. 20.40 crore in the auction. Among the six newcomers on the team are Alzarri Joseph, Yash Dayal, Lockie Ferguson, and Tom Curran. Joseph, bought for Rs 11.5 crore, is the team's costliest purchase. RCB has paid Rs 76.75 crore to retain 19 players, including Virat Kohli, Faf du Plessis, Mohammad Siraj, and Glenn Maxwell. <br/><br/>After the departure of Hardik Pandya, GT spent Rs 30.33 crore in the auction to strengthen the team, buying eight players, while retaining 17 for Rs. 61.85 crore. The team has bought Australian left-arm pacer Spencer Jhonson and all-rounder Shahrukh Khan for Rs 10 crore and Rs 7.4 crore, respectively. <br/><br/>The Lucknow Super Giants (LSG) spent only Rs 12 crore in the auction for six newcomers. The team has retained its core strengths, including KL Rahul, Quinton de Kock, and Marcus Stoinis, at Rs 86.85 crore. LSG is left with Rs 95 lakh in its purse after completing its 25-member squad. <br/><br/>PK have bought eight new players in the auction, of whom five are all-rounders. The team spent Rs 24.95 crore in the auction while retaining 17 players for Rs 70.90 crore. All-rounder Harshal Patel is the team's costliest purchase, whom it bought for Rs 11.75 crore.",
]

# Appending Forbes
news_articles = news_articles + forbes

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

# Appending Live Mint
for k in mint_live_updates:
    if len(mint_live_updates[k]) > 1:
        _string = (
            k.replace("IPL Auction 2024 Live Updates: ", "")
            + "\n"
            + "\n".join(mint_live_updates[k])
        )
    else:
        _string = (
            k.replace("IPL Auction 2024 Live Updates: ", "")
            + "\n"
            + mint_live_updates[k][0]
        )
    news_articles.append(_string)

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

# Appending IE Team review
news_articles = news_articles + ie_team_review

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

# Appending Mint Lounge
news_articles = news_articles + player_to_look_for

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

# Appending best buys
news_articles = news_articles + best_buys

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

# Appending ESPN
for k in espn_as_it_happens:
    if len(espn_as_it_happens[k]) > 1:
        _string = k + "\n" + "\n".join(espn_as_it_happens[k])
    else:
        _string = k + "\n" + espn_as_it_happens[k][0]
    news_articles.append(_string)


# Open the file in binary write mode
with open("ipl_2024_auction_news_article.pkl", "wb") as output_file:
    # Pickle the data object
    pickle.dump(news_articles, output_file)
