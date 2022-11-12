import scrapy
from crawler.crawler.items import Item_posters, Item_authors, Item_CVPR
from crawler.crawler.settings import WEBSITE,YEAR
#from scrapy.crawler import CrawlerProcess
#from scrapy.utils.project import get_project_settings

#--------------------FOR TESTING ONLY
#--------------------RUN THIS FILE 1ST TO EXTRACT DATA AND MAKE DIRECTORY--------------------
class Spiders_posters(scrapy.Spider):
    name = WEBSITE
    start_urls = []
    for year in YEAR:
        try:
            start_urls.append('https://%s.cc/Conferences/%d/Schedule?type=Poster'%(name,year))
        except:
            pass

    # ----------------------------------------Main Function-----------------------------------------------------
    def parse(self, response):
        id_list = response.css('.maincard.narrower.poster').getall()
        num_id_list = []
        for a in id_list:
            num_id_list.append(int(a.split('\n')[0].split('maincard_')[1][:-2]))

        min_id = min(num_id_list)
        max_id = max(num_id_list)
        #max_id = min_id + 9
        print(min_id, '+', max_id)
        # count_id = len(num_id_list)
        for id in range(min_id, max_id + 1):
            url = response.url.split('type')[0]+'showEvent=%d'%id
            # get posters, author info
            yield response.follow(url, callback=self.get_posters)

    # ----------------------------------------Other Function----------------------------------------------------
    def get_posters(self, response):
        posters = Item_posters()
        posters['id'] = self.name + response.url.split('/')[4][2:] + '-' + \
                        response.url.split('=')[1]
        posters['title'] = response.css('.maincardBody::text').get()
        posters['content'] = (response.css('.abstractContainer p::text').get() if response.css(
            '.abstractContainer p::text').get() is not None else response.css(
            '.abstractContainer::text').get() if response.css(
            '.abstractContainer::text').get() != "\n" else response.css('code::text').get())

        yield posters

class Spiders_authors(scrapy.Spider):
    name = WEBSITE
    start_urls = []
    for year in YEAR:
        try:
            start_urls.append('https://%s.cc/Conferences/%d/Schedule?type=Poster'%(name,year))
        except:
            pass

    # ----------------------------------------Main Function-----------------------------------------------------
    def parse(self, response):
        id_list = response.css('.maincard.narrower.poster').getall()
        num_id_list = []
        for a in id_list:
            num_id_list.append(int(a.split('\n')[0].split('maincard_')[1][:-2]))

        min_id = min(num_id_list)
        max_id = max(num_id_list)
        #max_id = min_id + 9
        print(min_id, '+', max_id)
        # count_id = len(num_id_list)
        for id in range(min_id, max_id + 1):
            url = response.url.split('type')[0]+'showEvent=%d'%id
            # get authors info
            yield response.follow(url, callback=self.get_authors)

    # ----------------------------------------Other Function----------------------------------------------------

    def get_authors(self, response):
        links = []
        numbers = [s for s in response.css('button.btn.btn-default').getall()[3:]]
        try:
            for a in numbers:
                links.append(response.url.split('showEvent')[0] + 'showSpeaker=%s' % a.split(';')[0].split('Speaker')[1][2:-2])
                print(links[-1])
        except Exception:
            pass
        for link in links:
            yield response.follow(link, callback=self.parse_school)

    def parse_school(self, response):
        authors = Item_authors()
        authors['poster_id'] = self.name+ response.url.split('/')[4][2:] + '-' + response.url.split('-')[-1]
        authors['author'] = response.css('h3::text').get()
        authors['work_place'] = response.css('h4::text').get()

        yield authors

class Spiders_CVPR(scrapy.Spider):
    name = "CVPR"
    start_urls = ['https://cvpr%d.thecvf.com' % year for year in YEAR]

    # ----------------------------------------Main Function-----------------------------------------------------
    def parse(self, response):
        for c in response.css('.nav-item.menu-item--collapsed a').getall():
            if len(c.split('Program'))==2:
                program = c.split('"')[1]
                break
        url = response.url+program
        yield response.follow(url, callback=self.to_program)

    # ----------------------------------------Other Function----------------------------------------------------

    def to_program(self, response): #go to Program tab from main page
        links = []
        for c in response.css('.dropdown-menu a').getall():
            if (len(c.split('Session'))==2 or len(c.split('Posters'))==2):
                links.append(response.url.split('.com')[0]+'.com'+c.split('"')[1])
        for link in links:
            yield response.follow(link, callback=self.to_schedule)

    def to_schedule(self, response): #go to Schedule tab from Program tab
        table = response.xpath('//*[@id="block-cvpr-content"]/div/article/div/div/table/tbody/tr')
        column = int(len(table[1].xpath('//td'))/len(table))
        for row in table[1:]:
            cvpr = Item_CVPR()
            cvpr['id'] = row.xpath('td[%d]//text()'%(column - 2)).extract_first()
            cvpr['title'] = row.xpath('td[%d]//text()' % (column - 1)).extract_first()
            author = row.xpath('td[%d]//text()' % column).extract()
            cvpr['author'] = (author[0] if author[0] != '\n\t\t\t' else author[1]).split('; ')
            yield cvpr