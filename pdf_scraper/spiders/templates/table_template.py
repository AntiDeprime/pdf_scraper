# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from pdf_scraper.items import PdfScraperItem
import json
from urllib.parse import urlparse, urljoin

class TableSpider(scrapy.Spider):

    def parse (self, response):
        
        self.logger.info('Moving to the page: %s', response.url)
        # Extract pdf page links 
        page_links = LinkExtractor(
            restrict_xpaths=self.url_xpath\
            ).extract_links(response)
        # Collect them
        for page in page_links:
            yield scrapy.Request (page.url, callback = self.parse_page)
        # When done, move to the next page 
        next_page_url = response.xpath(self.next_page_xpath).extract_first()
        # if url is not full 
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        next_page_url = urljoin(domain, next_page_url)
        if next_page_url:
            yield scrapy.Request (next_page_url, callback = self.parse)
        


    def parse_page(self, response):
        items = PdfScraperItem()

        # collect all data from table 
        json_dict = {}
        trs = response.xpath(self.table_xpath)
        for tr in trs:
            key = tr.xpath(self.table_categories_xpath).extract_first()
            value = tr.xpath(self.table_values_xpath).extract()
            value = ''.join(value)
            if key:
                if ':' in key:
                    pair = {key:value}
                    json_dict.update(pair)
                    
        # find and extract links to pdf files
        pdf_links = LinkExtractor(
            allow='(?i)\.pdf$',
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





            
            
            



