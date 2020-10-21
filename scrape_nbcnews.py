import pandas as pd
import random
import re
from tqdm import tqdm
from newspaper import Article


# nbcnews_success.csv is output from get_tweets.py script
df = pd.read_csv("./nbcnews_success.csv")

df['tweet_p'] = df['tweet'].apply(lambda x: re.sub("pic.twitter.com/[^ ]+","",x).strip())

all_stng = []
all_link = []

for t in list(df['tweet_p']):
    try:
        # This regex is specific to each of news handles
        m = re.search("nbcnews.to/", t)
        m = m.span()[0]

        stng = t[:m]
        link = t[m:]

        all_stng.append(stng)
        all_link.append(link)
    except:
        all_stng.append("")
        all_link.append("")

df['tweets_proc'] = all_stng
df['link'] = all_link

df['tweets_proc'] = df['tweets_proc'].apply(lambda x: x.strip())

df['link'] = df['link'].apply(lambda x: x.strip())
df['link'] = df['link'].apply(lambda x: "https://"+x)
df = df[df['link']!="https://"]

save_text = []
save_meta = []
save_title = []
save_is_media = []
save_is_parsed = []
save_author = []
save_link = []

for l in tqdm(list(df['link'])):

    try:
        art = Article(l)

        art.download()
        art_html = art.html
        art.parse()

        save_text.append(art.text)
        save_meta.append(art.meta_data)
        save_title.append(art.title)
        save_is_media.append(art.is_media_news())
        save_is_parsed.append(art.is_parsed)
        save_author.append(art.authors)
        save_link.append(art.canonical_link)
    except:
        print("error", l)

        save_text.append(None)
        save_meta.append(None)
        save_title.append(None)
        save_is_media.append(None)
        save_is_parsed.append(None)
        save_author.append(None)
        save_link.append(None)

df['article_text'] = save_text
df['article_meta'] = save_meta
df['article_title'] = save_title
df['is_media'] = save_is_media
df['is_parsed'] = save_is_parsed
df['author'] = save_author
df['full_link'] = save_link

df.to_json("./nbcnews_success_articles.json")

