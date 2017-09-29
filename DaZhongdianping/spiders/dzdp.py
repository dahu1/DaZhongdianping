# -*- coding: utf-8 -*-
import scrapy


class DzdpSpider(scrapy.Spider):
    name = 'dzdp'
    start_urls = ['http://www.dianping.com/shop/8065409/review_more']

    def parse(self, response):
        print '>>run!'
        for i in response.xpath('//div[@class="content"]'):
            for j in i.xpath('.//div[@class="J_brief-cont"]/text()').extract():
                print j.strip()
        pass
