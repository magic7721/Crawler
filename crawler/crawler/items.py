# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Item_posters(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
class Item_authors(scrapy.Item):
    # define the fields for your item here like:
    poster_id = scrapy.Field()
    author = scrapy.Field()
    work_place = scrapy.Field()
class Item_CVPR(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()

