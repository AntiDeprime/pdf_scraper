# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from pdf_scraper.items import PdfScraperItem
import logging 
import json


class UnescopdfSpider(scrapy.Spider):
    
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
    def parse (self, response):
        
        self.logger.info('Moving to the page: %s', response.url)
        # Extract pdf page links 
        page_links = LinkExtractor(
            allow_domains='unesco.org',
            restrict_xpaths='//span[@class="record"]'\
            ).extract_links(response)
        # Collect them
        for page in page_links:
            yield scrapy.Request (page.url, callback = self.parse_page)
        # When done, move to the next page 
        next_page_url = response.xpath("//a[text()='[next]']/@href").extract_first()
        if next_page_url:
            yield scrapy.Request (next_page_url, callback = self.parse)
        



    def parse_page(self, response):
        items = PdfScraperItem()

        # collect all data from table 
        json_dict = {}
        trs = response.xpath('//table//tr')
        for tr in trs:
            key = tr.xpath('td[1]//text()').extract_first()
            value = tr.xpath('td[2]//text()').extract()
            value = ''.join(value)
            if key:
                if ':' in key:
                    pair = {key:value}
                    json_dict.update(pair)
                    
        # find and extract links to pdf files
        pdf_links = LinkExtractor(
            allow='\.pdf$',
            allow_domains='unesdoc.unesco.org',
            deny_extensions='').extract_links(response)

        # get link urls as list
        pdf_link_list = []
        for link in pdf_links:
            pdf_link_list.append(link.url)

        # Remove newlines from json data 
        for key, value in json_dict.items():
            json_dict[key] = ' '.join(value.split())
        
        # Create scrapy items 
        items['url'] = response.url
        items['pdf_links'] = pdf_link_list
        items['json_data'] = json.dumps(json_dict, ensure_ascii=False).encode('utf8')

        # return only if everything is found
        if (items['url'] and items['pdf_links'] and items['json_data']):
            self.logger.info("Success! %s", response.url)
            return items





            
            
            
