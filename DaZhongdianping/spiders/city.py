# -*- coding: utf-8 -*-
import scrapy,sys
reload(sys)
sys.setdefaultencoding("utf-8")

class CitySpider(scrapy.Spider):
    name = 'city'
    start_urls = ['http://www.dianping.com/citylist']

    def parse(self, response):
        with open('city','a')as f:
            for i in response.xpath('//ul[@class="glossary-list gl-py"]/li/div[@class="terms"]/a'):
                a= i.xpath('./strong/text()').extract_first() or i.xpath('./text()').extract_first()
                f.write(a+'\n')
        pass
