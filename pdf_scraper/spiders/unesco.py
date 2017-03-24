# -*- coding: utf-8 -*-
from pdf_scraper.spiders.templates.table_template import TableSpider


class UnescoSpider(TableSpider):
    
    # custom settings only for this spider
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'CONCURRENT_REQUESTS': 10,
                       'DOWNLOAD_DELAY': 2,
                       }
    name = "unesco"
    allowed_domains = ["unesco.org"]
    start_urls = (
        'http://www.unesco.org/ulis/cgi-bin/ulis.pl?req=0&mt2=100&mt2_p=%3C&by=2&sc1=1&look=default&sc2=1&lin=1&futf8=1&gp=1&hist=1&pn=1&mt=3%2C1%2C5%2C6%2C12%2C7%2C10&mtX=3&mtX=1&mtX=5%2C6&mtX=12&mtX=7&mtX=10&pdf=1&tx=&tx_p=near&ti=&ti_p=inc&text=&text_p=phrase+words&ds=&ds_tie=and&ds_2=&au=&la=&dafr=&dato=&dc=&ib=&submit=Ok',
    )

    table_xpath = '//table//tr'
    table_categories_xpath = 'td[1]//text()'
    table_values_xpath = 'td[2]//text()'
    url_xpath = '//span[@class="record"]'
    next_page_xpath = "//a[text()='[next]']/@href"
