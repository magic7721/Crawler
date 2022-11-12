from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from website_crawler import Spiders_posters,Spiders_authors, Spiders_CVPR
from search_api import Arxiv_api,Wiki_api, Arxiv_api2
from GUI import GUI
from schema import Table_builder
from multiprocessing import Process
from crawler.crawler.settings import WEBSITE
import os,shutil

import timeit
start = timeit.default_timer()

class final_product():
    def __init__(self):
        if os.path.exists('%s'%WEBSITE):
            shutil.rmtree('%s'%WEBSITE)
        os.mkdir('%s'%WEBSITE)
    def first_step(self):
        #RUN THIS FILE 1ST TO EXTRACT DATA AND MAKE DIRECTORY
        first_start = timeit.default_timer()
        process = CrawlerProcess(get_project_settings())
        if WEBSITE != "CVPR":
            process.crawl(Spiders_posters)
            process.crawl(Spiders_authors)
        else:
            process.crawl(Spiders_CVPR)
        process.start()
        first_stop = timeit.default_timer()
        print('1st step time: ', first_stop - first_start)
        self.second_step(first_stop - first_start)
    def second_step(self, first_time=float(0)):
        #RUN THIS FOR TESTING
        second_start = timeit.default_timer()
        if WEBSITE != "CVPR":
            arxi = Arxiv_api2()
            wiki = Wiki_api()
            p1 = Process(target=arxi.search_arxiv)
            p1.start()
            p2 = Process(target=wiki.search_wiki)
            p2.start()
            p1.join()
            p2.join()
        else:
            arxi = Arxiv_api2()
            arxi.search_arxiv()
        second_stop = timeit.default_timer()
        print('2nd step time: ', second_stop - second_start)
        self.third_step(first_time, second_stop - second_start)

    def test_step(self, first_time=float(0)):
        #FOR TESTING ARXIV API
        second_start = timeit.default_timer()
        arxi = Arxiv_api()
        arxi.search_arxiv()
        second_stop = timeit.default_timer()
        print('2nd step time: ', second_stop - second_start)
        #self.third_step(first_time, second_stop - second_start)
    def third_step(self, first_time=float(0), second_time=float(0)):
        #RUN THIS FILE 3RD TO BUILD RELATION TABLE
        third_start = timeit.default_timer()
        table = Table_builder()
        table.execute()
        third_stop = timeit.default_timer()
        print('1st step time: ', first_time)
        print('2nd step time: ', second_time)
        print('3rd step time: ', third_stop - third_start)

def build_database():
    b = final_product()
    b.test_step()
def sqlite_query():
    GUI()

if __name__ == '__main__':
    sqlite_query()
    stop = timeit.default_timer()
    #average time : 2s per paper
    # nips.cc 2021,2022 have 7304 papers, total time estimated at 15300s (4h 15m) + 3h waiting during timeout -> 7h
    print('Total time: ', stop - start)