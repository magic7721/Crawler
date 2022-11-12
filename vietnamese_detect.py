from langdetect import detect
import pandas as pd
import json
from gensim.utils import tokenize
import numpy as np

authors = pd.DataFrame(json.load(open('crawler/crawler/spiders/NIPS/authors.json', encoding='utf-8')))
languages = authors[['author']]
languages=languages.drop_duplicates().reset_index(drop=True)
languages['language'] = np.nan

def lang_categorize(text):
    names = [text] + list(tokenize(text))
    nvi = 0
    vi = 0
    for name in names:
        if detect(name) == 'vi':
            vi+=1
        else:
            nvi+=1
    if vi> 2*nvi:
        print(text)
        return "Vietnamese"
    else:
        return "Foreign"

languages['language'] = languages.apply(lambda row: lang_categorize(row['author']),axis=1)
languages.to_json('crawler/crawler/spiders/languages.json', orient='records', lines=True)