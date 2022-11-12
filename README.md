# Turorial

- in settings.py, change WEBSITE value to 'NIPS', 'ICML', ICLR' or 'CVPR' (coresponding to databases currently in folder)

- run function __sqlite_query()__ in /spiders/__ init __ .py

- it is basically an sqlite simulator, just query it like sqlite

# Building new Database from website

- in settings.py, change WEBSITE and YEAR values (default website is 'ICLR' (iclr.cc), year is [2021,2022])

- run function __build_database()__ in /spiders/__ init __ .py

- __WARNING__, it will __DELETE__ existing __DATABASE__ if the names match

# Explaining files

- website_crawler.py: web crawler using Scrapy library, scrape site for data

- search_api.py: web crawler using arxiv and wikipedia api, search for extra info

- schema.py: build relation tables

- GUI.py: interface

- test.py: random stuffs

# Using scrapy in terminal

- for "scrapy crawl" command, open terminal in /spiders

- for anything else, open terminal in root folder



