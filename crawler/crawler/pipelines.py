# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import JsonLinesItemExporter
from crawler.crawler.items import Item_posters,Item_authors

class CrawlerPipeline:
    def process_item(self, item, spider):

        if isinstance(item, Item_posters):
            filename = item['id'].split("2")[0]
            print(filename)
            export = JsonLinesItemExporter(open(filename + '/posters.json', "ab")).export_item(item)
        elif isinstance(item, Item_authors):
            filename = item['poster_id'].split("2")[0]
            print(filename)
            export = JsonLinesItemExporter(open(filename + '/authors.json', "ab")).export_item(item)
        else:
            filename = "CVPR"
            print(filename)
            authors = {key: item[key] for key in item.keys() & {'id', 'author'}}
            authors['poster_id'] = authors.pop('id')
            authors['author'] = authors.pop('author')
            item.pop('author')
            export = JsonLinesItemExporter(open(filename + '/posters.json', "ab")).export_item(item)
            export2 = JsonLinesItemExporter(open(filename + '/authors.json', "ab")).export_item(authors)

        return item
