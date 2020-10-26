import pandas as pd
import numpy as np
import os

import warnings

import re
import nltk

warnings.filterwarnings('ignore')

files = os.listdir("./")
files = [a for a in files if ".json" in a]

path = "../twitter_news_data/"
pds = []
for f in files:
    df = pd.read_json(f)
    pds.append(df)
    
df_all = pd.concat(pds)
df_all_samp = df_all[['tweets_proc', 'article_text', 'article_title']]

df_all_samp.dropna(inplace=True)
df_all_samp.drop_duplicates(inplace=True)

def clean(x):
    x = x.replace("\n"," ")
    x = x.replace("\\","")
    x = re.sub(" +"," ",x)
    try:
        a = re.search("^[A-Za-z ]+\|[a-zA-Z\-\. ]+: ", x)
        a = a.span()
        x = x[a[1]:]
    except:
        pass
    try:
        a = re.search("^[A-Za-z@\.]+: ", x)
        a = a.span()
        x = x[a[1]:]
    except:
        pass
    try:
        a = re.search("- @",x)
        a = a.span()
        x = x[:a[0]]
    except:
        pass
    
    try:
        a = re.search("^[A-Z ]+: ", x)
        a = a.span()
        x = x[a[1]:]
    except:
        pass
        
    try:
        a = re.search(",[a-zA-Z ]+ tell[a-zA-Z ]+@[a-zA-Z\.]+", x)
        a = a.span()
        x = x[:a[0]]+x[a[1]:]
    
    except:
        pass
    try:
        a = re.search(",[a-zA-Z ]+ told[a-zA-Z ]+@[a-zA-Z]+", x)
        a = a.span()
        x = x[:a[0]]+x[a[1]:]
    
    except:
        pass
    
    try:
        a = re.search(",[\"] according[a-zA-Z ]+@[a-zA-Z]+", x)
        a = a.span()
        x = x[:a[0]]+x[a[1]:]
    
    except:
        pass
    
    try:
        a = re.search("Reporting by @[a-zA-Z\.: ]+", x)
        a = a.span()
        x = x[:a[1]]
    
    except:
        pass
    
    try:
        a = re.search("Via .+", x)
        a = a.span()
        x = x[:a[0]]
    
    except:
        pass
    try:
        a = re.search("via .+", x)
        a = a.span()
        x = x[:a[0]]
    
    except:
        pass
    
    
    try:
        a = re.search("^@[a-zA-Z]+: \"", x)
        a = a.span()
        x = "Fact check: "
    
    except:
        pass
    
    try:
        a = re.search("^@[a-zA-Z]+: ", x)
        a = a.span()
        x = x[a[1]:]
    
    except:
        pass

    try:
        a = re.search("More from .+", x)
        a = a.span()
        x = x[:a[0]]
    
    except:
        pass
    try:
        a = re.search("Analysis [@a-zA-Z ]+:", x)
        a = a.span()
        x = x[:a[0]]+x[a[1]:]
    
    except:
        pass
    
    try:
        a = re.search("LIVE", x)
        a = a.span()
        x = ""
    
    except:
        pass
    
    x = x.replace("Fact check: ", "")
    x = x.replace("JUST IN: ", "")
    x = x.replace("Fact Check: ", "")
    
    return x
    
    
df_all_samp['tweets_proc_now'] = df_all_samp['tweets_proc'].apply(lambda x: clean(x))
