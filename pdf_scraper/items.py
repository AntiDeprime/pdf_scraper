# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PdfScraperItem(scrapy.Item):
    url = scrapy.Field()
    pdf_links  = scrapy.Field()
    json_data = scrapy.Field()
