# -*- coding: utf-8 -*-
from pdf_scraper.spiders.templates.table_template import TableSpider


class WhoSpider(TableSpider):
    # custom settings only for this spider
    custom_settings = {'ROBOTSTXT_OBEY': True,
                       'CONCURRENT_REQUESTS': 10,
                       'DOWNLOAD_DELAY': 2,
                       }
    name = "who"
    allowed_domains = ["apps.who.int"]
    start_urls = (
        'http://apps.who.int/iris/browse?type=dateissued',
    )
    table_xpath = '//table//tr'
    table_categories_xpath = 'td[1]//text()'
    table_values_xpath = 'td[2]//text()'
    url_xpath = '//a[contains(@class, "list-results")]'
    next_page_xpath = "//a[@class='pull-right']/@href"
