# -*- coding: utf-8 -*-
import scrapy, sys, os
from scrapy import Request
from DaZhongdianping.items import DazhongdianpingItem

reload(sys)
sys.setdefaultencoding("utf-8")


class SitemapSpider(scrapy.Spider):
    name = 'sitemap'
    start_urls = ['https://www.dianping.com/sitemap/c1c10']

    def parse(self, response):
        total_country_sitemap = response.xpath('//div[@class="navigation"]')[2]
        for i in total_country_sitemap.xpath('./div[@class="nav-category"]//div[@class="nc-items"]/a'):
            sitemap_name = i.xpath('./span/text()').extract_first()
            sitemap_src = i.xpath('./@href').extract_first()
            shanghai = 'https://www.dianping.com/sitemap/c1c10'
            yield Request(response.urljoin(sitemap_src), callback=self.sitemap_parse, meta={'sitemap_name': sitemap_name})
            # yield Request(shanghai, callback=self.sitemap_parse, meta={'sitemap_name': sitemap_name})
        pass

    def sitemap_parse(self, response):
        sitemap_name = response.meta['sitemap_name']
        total_kind_sitemap = response.xpath('//div[@class="navigation"]')[0]
        for i in total_kind_sitemap.xpath('.//div[@class="nc-items nc-more"]/a'):
            sitemap_kind_name = i.xpath('./span/text()').extract_first()
            sitemap_kind_src = i.xpath('./@href').extract_first()
            path = sitemap_name + ' >> ' + sitemap_kind_name
            yield Request(sitemap_kind_src, callback=self.area_parse, meta={'path': path})
            shanghai_jiachangcai = 'http://www.dianping.com/search/category/1/10/g1783'
            # yield Request(shanghai_jiachangcai, callback=self.area_parse, meta={'path': path})
        pass

    def area_parse(self, response):
        path = response.meta['path']
        # sitemap_name = response.meta['sitemap_name']
        # 地域不限的先爬
        for i in response.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li'):
            info = {'path': path}
            info['shop_title'] = i.xpath('./div[@class="txt"]/div[@class="tit"]/a/@title').extract_first()
            info['mean_price'] = i.xpath(
                './div[@class="txt"]/div[@class="comment"]/a[@class="mean-price"]/b/text()').extract_first()
            info['review_num'] = i.xpath(
                './div[@class="txt"]/div[@class="comment"]/a[@class="review-num"]/b/text()').extract_first()
            info['address'] = i.xpath(
                './div[@class="txt"]/div[@class="tag-addr"]/span[@class="addr"]/text()').extract_first()
            info['added_info'] = i.xpath('./div[@class="svr-info"]/a/@title').extract()
            info['shop_src'] = i.xpath('./div[@class="txt"]/div[@class="tit"]/a/@href').extract_first()
            print info['shop_title'],info['shop_src']
            yield Request(info['shop_src'], callback=self.shop_full_infomation,meta={'info': info})
            douyue = 'http://www.dianping.com/shop/58840610'
            # yield Request(douyue, callback=self.shop_full_infomation, meta={'info': info})
        next_page = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract_first()
        # 开启下一页
        if next_page != None:
            # print '>>>next Page!',response.xpath('//div[@class="page"]/a[@class="next"]/@data-ga-page').extract_first()
            yield Request(next_page,callback=self.area_parse,meta={'path': path})
            pass

        # 然后各个地域的再爬
        for i in response.xpath('//div[@class="nav-category nav-tabs J_filter_region"]//div[@id="J_nt_items"]//a'):
            area_name = i.xpath('./span/text()').extract_first()
            area_src = i.xpath('./@href').extract_first()
            # print area_name
            yield Request(area_src, callback=self.shop_list_parse,meta={'path': path})
            pudong = 'http://www.dianping.com/search/category/1/10/g1783r5'
            # yield Request(pudong, callback=self.shop_list_parse, meta={'path': path})
        pass

    def shop_list_parse(self, response):
        path = response.meta['path']
        for i in response.xpath('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li'):
            info = {'path': path}
            info['shop_title'] = i.xpath('./div[@class="txt"]/div[@class="tit"]/a/@title').extract_first()
            info['mean_price'] = i.xpath(
                './div[@class="txt"]/div[@class="comment"]/a[@class="mean-price"]/b/text()').extract_first()
            info['review_num'] = i.xpath(
                './div[@class="txt"]/div[@class="comment"]/a[@class="review-num"]/b/text()').extract_first()
            info['address'] = i.xpath(
                './div[@class="txt"]/div[@class="tag-addr"]/span[@class="addr"]/text()').extract_first()
            info['added_info'] = i.xpath('./div[@class="svr-info"]/a/@title').extract()
            info['shop_src'] = i.xpath('./div[@class="txt"]/div[@class="tit"]/a/@href').extract_first()
            print info['shop_title'],info['shop_src']
            yield Request(info['shop_src'], callback=self.shop_full_infomation, meta={'info': info})
        next_page = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract_first()
        # 开启下一页
        if next_page != None:
            print '>>>next Page!', response.xpath('//div[@class="page"]/a[@class="next"]/@data-ga-page').extract_first()
            yield Request(next_page, callback=self.shop_list_parse, meta={'path': path})

        pass

    def shop_full_infomation(self, response):
        info = response.meta['info']
        item=DazhongdianpingItem()
        item['_id']=info['shop_src']
        print info['shop_title'],'shop_full_infomation'
        basic_info = response.xpath('//div[@id="basic-info"]')
        shop_name = basic_info.xpath('./h1[@class="shop-name"]/text()').extract_first().strip()
        # 评分
        info['comment_score'] = basic_info.xpath('./div[@class="brief-info"]/span[@id="comment_score"]/span/text()').extract()
        info['street_address'] = basic_info.xpath(
            './div[@class="expand-info address"]/span[@itemprop="street-address"]/text()').extract_first().strip()
        info['tel'] = basic_info.xpath('./p[@class="expand-info tel"]/span[@itemprop="tel"]/text()').extract_first()
        info['hide_info'] = basic_info.xpath('./div[@class="other J-other Hide"]/p/span[@class="item"]/text()').extract_first()
        item['info']=info
        recommend_dish_src = os.path.join(response.url, 'dishlist')
        yield Request(recommend_dish_src, callback=self.shop_recommend_dish, meta={'item': item})
        shop_comment_src = os.path.join(response.url, 'review_more')
        yield Request(shop_comment_src, callback=self.shop_comment, meta={'item': item})
        yield item

    def shop_recommend_dish(self, response):
        item= response.meta['item']
        print item['info']['shop_title'],'shop_recommend_dish'
        recommend_dish=item['recommend_dish'] if "recommend_dish"  in item else []
        for i in response.xpath('//div[@class="shop-food-list"]/div[@class="list-desc"]/ul/a'):
            # print i.xpath('./div[@class="shop-food-con"]/div[@class="shop-food-name"]/text()').extract_first()
            recommend_dish.append(i.xpath('./div[@class="shop-food-con"]/div[@class="shop-food-name"]/text()').extract_first())
        item['recommend_dish']=recommend_dish
        next_page = response.xpath('//div[@class="shop-food-list-page"]/a[@class="next"]/@href').extract_first()
        if next_page!=None:
            next_page=response.urljoin(next_page)
            # print '>>>next Page!', response.xpath('//div[@class="shop-food-list-page"]/a[@class="next"]/@data-ga-page').extract_first()
            yield Request(next_page, callback=self.shop_recommend_dish,meta={'item': item})
        yield item

    def shop_comment(self, response):
        item = response.meta['item']
        print item['info']['shop_title'], 'shop_comment'
        comment = item['comment'] if "comment" in item else []
        for i in response.xpath('//div[@class="content"]'):
            for j in i.xpath('.//div[@class="J_brief-cont"]/text()').extract():
                comment.append(j.strip())
                # print j.strip()
                pass
        item['comment']=comment
        next_page = response.xpath(
            '//div[@class="Pages"]/div[@class="Pages"]/a[@class="NextPage"]/@href').extract_first()
        if next_page != None:
            next_page = response.urljoin(next_page)
            # print '>>>next Page!', response.xpath('//div[@class="Pages"]/div[@class="Pages"]/a[@class="NextPage"]/@data-pg').extract_first()
            yield Request(next_page, callback=self.shop_comment,meta={'item': item})
        yield item
