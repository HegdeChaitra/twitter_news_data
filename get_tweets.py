import twint
import pandas as pd
import numpy as np

from datetime import datetime
from datetime import timedelta

users_list = ["CNN", "nytimes", "theatlantic", "newyorker", "HuffingtonPost", "FoxNews", "ABC",
             "washingtonpost", "TIME", "Newsweek", "USATODAY", "VOANews", "WSJ", "NOLAnews",
             "CBSNews", "Suntimes", "TB_Times", "HoustonChron", "latimes", "phillydotcom", "njdotcom",
             "dallasnews", "ajc", "usnews", "reuters", "nydailynews", "nypost", "suntimes", "chicagotribune",
              "newsday", "ocregister", "starledger", "clevelanddotcom", "phillyinquirer", "startribune",
              "guardian", "IrishTimes", "thesun", "mailonline", "dailymailuk", "dailymail", "theeconomist",
             "thescotsman", "independent", "ajenglish"]

def get_tweet(config):
    twint.run.Search(config)
    tlist = config.search_tweet_list

    return tlist

for usr in np.unique(users_list):

    if usr in ['ABC', 'CBSNews']:
        continue
    print(usr)
    c = twint.Config()
    c.Search = "from:@"+usr
    c.Store_object = True
    c.Limit = 50

    start_date = "2019-01-01"
    stop_date = "2020-10-07"

    start = datetime.strptime(start_date, "%Y-%m-%d")
    stop = datetime.strptime(stop_date, "%Y-%m-%d")

    output_tweets = []
    while start < stop:
        print(start)
        next_day = start + timedelta(days=1)

        c.Since = str(start)
        c.Until = str(next_day)
        start = next_day

        output_tweets+=get_tweet(c)

    df = pd.DataFrame(output_tweets)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.to_csv("./{}_success.csv".format(usr), index=False)
    print(df.shape[0])
    print()

