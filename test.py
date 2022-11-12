# random stuff here
import pandas as pd
import json
import time
import os

posters = pd.DataFrame([json.loads(line) for line in
                                open('crawler/crawler/spiders/NIPS/posters.json', 'r', encoding='utf-8')])
print(posters.shape[0])
posters=posters.dropna()
posters=posters[['id','title']].drop_duplicates().reset_index(drop=True)
posters=posters.sort_values(by=['id'], ignore_index=True)
print(posters.shape[0])

