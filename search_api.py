import json
import time

import pandas as pd
import numpy as np
import arxiv
from difflib import SequenceMatcher
import wikipedia
from gensim.utils import tokenize
from crawler.crawler.settings import WEBSITE
from multiprocessing import Process

#--------------------FOR TESTING ONLY
#--------------------RUN THIS FILE 2ND TO EXTRACT MORE DATA--------------------


#get info from arxiv and wikipedia
class Arxiv_api():

    def search_arxiv(self, input_file="%s/posters.json"%WEBSITE, output_file = "%s/additional2.json"%WEBSITE):
        processed_file = self.__process(input_file) # posters.json
        self.__output(processed_file, output_file) # additional.json
    def __similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    def __process(self, input_file):
        if WEBSITE == "CVPR":
            authors = pd.DataFrame([json.loads(line) for line in
                                    open('%s/authors.json'%WEBSITE, 'r', encoding='utf-8')])
            authors=authors.explode('author')
            authors.to_json('%s/authors.json'%WEBSITE, orient='records', lines=True)

        #load posters data
        posters = pd.DataFrame([json.loads(line) for line in
                                open('%s'%input_file, 'r', encoding='utf-8')])
        posters=posters.dropna()
        posters=posters[['id','title']].drop_duplicates().reset_index(drop=True)
        posters=posters.sort_values(by=['id'], ignore_index=True)
        print(posters.shape[0])

        posters_extra=pd.DataFrame({'id':posters['id']})
        titles=posters['title']

        posters_extra['date']=np.nan
        posters_extra['categories'] = posters_extra.apply(lambda x: [], axis=1)
        posters_extra['primary_cat']=np.nan

        second = 60
        for index in range(posters.shape[0]):
            retry = 0
            while retry <= 6:
                try:
                    print('indexing...')
                    query = titles[index].strip()
                    search = arxiv.Search(query=query, max_results=3)
                    for a in search.results():
                        print('index: ', index)
                        if self.__similar(a.title, query) > 0.5:
                            posters_extra.loc[index,['date','categories','primary_cat']]=[str(a.published), a.categories,a.primary_category]
                            break
                    break
                except Exception as e:
                    retry += 1
                    if retry >= 2:
                        second += 60
                    print('failed index ',index,': ', e)
                    for i in range(10, 0, -1):
                        print('Timeout, process will resume after %d minutes...' % int(i*(second/60)))
                        time.sleep(second)
                    print("Continuing...")
            if retry >= 6:
                break

        return posters_extra
    def __output(self, processed_file, output_file):
        processed_file.to_json('%s'%output_file, orient='records', lines=True)

class Wiki_api():

    def search_wiki(self, input_file = "%s/authors.json"%WEBSITE, output_file = "%s/work_categories.json"%WEBSITE):
        processed_file = self.__process(input_file) # authors.json
        self.__output(processed_file, output_file) # work_categories.json

    __institute_list = ["univer", "institu", "college", "polyte", "inria", "school", "academ", "harvard", "upérieure", "oxford", "stanford", "hornell"]
    def __process(self, input_file):
        #load author data
        authors = pd.DataFrame([json.loads(line) for line in
                                open('%s'%input_file, 'r', encoding='utf-8')])

        work_categories = authors[['work_place']]
        work_categories=work_categories.dropna().drop_duplicates().reset_index(drop=True)
        work_categories['work_type'] = np.nan

        work_categories['work_type'] = work_categories.apply(lambda row: self.__work_type_categorize(str(row['work_place'])),axis=1)
        return work_categories

    def __work_type_categorize(self, text):
        if any(name in text.lower() for name in self.__institute_list):
            return "Institute"
        else:
            try:
                queries = [text]+list(tokenize(text))
                for query in queries:
                    if any(name in wikipedia.search(query)[0].lower() for name in self.__institute_list):
                        print(query)
                        return "Institute"
                return "Company"
            except Exception as e:
                print(e)
                return 'Company'
    def __output(self,processed_file, output_file):
        processed_file.to_json('%s'%output_file, orient='records', lines=True)

class Arxiv_api2(): #Arxiv api is unusable. It timeout from the start. So, no waiting, just break.

    def search_arxiv(self, input_file="%s/posters.json"%WEBSITE, output_file = "%s/additional.json"%WEBSITE):
        processed_file = self.__process(input_file) # posters.json
        self.__output(processed_file, output_file) # additional.json
    def __similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    def __process(self, input_file):
        if WEBSITE == "CVPR":
            authors = pd.DataFrame([json.loads(line) for line in
                                    open('%s/authors.json'%WEBSITE, 'r', encoding='utf-8')])
            authors=authors.explode('author')
            authors.to_json('%s/authors.json'%WEBSITE, orient='records', lines=True)

        #load posters data
        posters = pd.DataFrame([json.loads(line) for line in
                                open('%s'%input_file, 'r', encoding='utf-8')])
        posters=posters.dropna()
        posters=posters[['id','title']].drop_duplicates().reset_index(drop=True)
        posters=posters.sort_values(by=['id'], ignore_index=True)
        print(posters.shape[0])

        posters_extra=pd.DataFrame({'id':posters['id']})
        titles=posters['title']

        posters_extra['date']=np.nan
        posters_extra['categories'] = posters_extra.apply(lambda x: [], axis=1)
        posters_extra['primary_cat']=np.nan

        for index in range(posters.shape[0]):
            try:
                print('indexing...')
                query = titles[index].strip()
                search = arxiv.Search(query=query, max_results=3)
                for a in search.results():
                    print('index: ', index)
                    if self.__similar(a.title, query) > 0.5:
                        posters_extra.loc[index,['date','categories','primary_cat']]=[str(a.published), a.categories,a.primary_category]
                        break
                    break
            except:
                break

        return posters_extra
    def __output(self, processed_file, output_file):
        processed_file.to_json('%s'%output_file, orient='records', lines=True)
