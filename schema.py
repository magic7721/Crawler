import pandas as pd
import sqlite3
import json
from prettytable import PrettyTable,ALL
import textwrap
from crawler.crawler.settings import WEBSITE
import numpy as np

#--------------------FOR TESTING ONLY
#--------------------RUN THIS FILE 3RD TO BUILD RELATION TABLE--------------------

class Table_builder():

    def __init__(self, name = WEBSITE): #name of folder containing json files Example: NIPS
        self.name = name
        self.__build()

    def __load_data(self):

        authors = pd.DataFrame([json.loads(line) for line in open(self.name+'/authors.json', 'r', encoding='utf-8')])
        posters = pd.DataFrame([json.loads(line) for line in open(self.name + '/posters.json', 'r', encoding='utf-8')])

        dates_categories = pd.DataFrame([json.loads(line) for line in open(self.name+'/additional.json', 'r', encoding='utf-8')])
        dates_categories=dates_categories.dropna().reset_index(drop=True)

        dates=dates_categories[['id','date']]

        categories=dates_categories[['id','categories','primary_cat']]
        categories=categories.explode('categories')
        categories['primary_categories']=np.nan
        try:
            categories['primary_categories'] = categories.apply(lambda row: row['categories']==row['primary_cat'],axis=1)
        except:
            pass
        categories=categories.drop(columns='primary_cat')
        work_categories = ''
        if WEBSITE != "CVPR":
            work_categories = pd.DataFrame([json.loads(line) for line in open(self.name + '/work_categories.json', 'r',encoding='utf-8')])

        # see people with same name
        # author=author.drop_duplicates()
        # ids = author["author"]
        # pd.options.display.max_rows = 1000
        # print(author[ids.isin(ids[ids.duplicated()])].sort_values("author"))

        return   posters, authors, dates, categories, work_categories

    def __build(self):

        posters, authors, dates, categories, work_categories = self.__load_data()

        con = sqlite3.connect(self.name+'/'+self.name+'.db')
        cur = con.cursor()
        cur.executescript('''
                    CREATE TABLE IF NOT EXISTS posters (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL
                        );
                        
                    CREATE TABLE IF NOT EXISTS dates (
                        id INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        FOREIGN KEY(id) REFERENCES posters(id)
                        );
                        
                    CREATE TABLE IF NOT EXISTS fields (
                        id INTEGER NOT NULL,
                        categories TEXT NOT NULL,
                        primary_categories BOOL NOT NULL,
                        FOREIGN KEY(id) REFERENCES posters(id)
                        );
                    ''')
        if work_categories is not '':
            cur.executescript('''
                        CREATE TABLE IF NOT EXISTS authors (
                            poster_id INTEGER NOT NULL,
                            author TEXT NOT NULL,
                            work_place TEXT,
                            FOREIGN KEY(poster_id) REFERENCES posters(id)
                            );
                                     
                        CREATE TABLE IF NOT EXISTS work_categories (
                            work_place TEXT NOT NULL,
                            work_type TEXT NOT NULL,
                            FOREIGN KEY(work_place) REFERENCES authors(work_place)
                            );      
                        ''')
        else:
            cur.executescript('''
                        CREATE TABLE IF NOT EXISTS authors (
                            poster_id INTEGER NOT NULL,
                            author TEXT NOT NULL,
                            FOREIGN KEY(poster_id) REFERENCES posters(id)
                            );                                
                        ''')

        posters.to_sql('posters', con, if_exists='replace', index = False)
        authors.to_sql('authors', con, if_exists='replace', index = False)
        dates.to_sql('dates', con, if_exists='replace', index = False)
        categories.to_sql('fields', con, if_exists='replace', index = False)
        if work_categories is not '':
            work_categories.to_sql('work_categories', con, if_exists='replace', index = False)

        con.close()

    def execute(self, query = '''
                    SELECT b.id, b.title, a.author FROM posters b, authors a 
                    WHERE a.poster_id = b.id
                    ORDER BY b.id
                    LIMIT 10
                  '''):
                    #select work_type, round(count(*) * 100.0 / (select count(*) from work_categories), 2)
                    #from work_categories
                    #group by work_type
        con = sqlite3.connect(self.name + '/' + self.name + '.db')
        cur = con.cursor()
        db = cur.execute(query)
        myTable = PrettyTable()
        myTable.hrules = ALL
        wrapper = textwrap.TextWrapper(width=50)
        for c in cur.fetchall():
            myTable.add_row(c)
        print(myTable)

        con.close()