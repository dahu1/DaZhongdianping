# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class DazhongdianpingPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient('localhost', 27017)
        # self.client = MongoClient('115.159.157.136', 27017)
        self.db = self.client['dazhong_dianping']
        self.db["dz"].drop()
        self.db["recommend_dish"].drop()
        self.db["comment"].drop()
        self.db["basic"].drop()
        # self.db['零度君上'].delete_many({})
        pass

    def process_item(self, item, spider):
        # self.db['零度君上'].insert_one(dict(item))    #注意这里是一个个插入,insert_many会报错
        dbname = 'dz'
        # if self.db[dbname].find({"_id": item['_id']}).count():
        if 'recommend_dish' in item:
            self.db['recommend_dish'].update_one({'_id': item['_id']}, {"$set":  item},upsert=True)
        elif 'comment' in item:
            self.db['comment'].update_one({'_id': item['_id']}, {"$set": item}, upsert=True)
        else:
            self.db['basic'].update_one({'_id': item['_id']}, {"$set": item}, upsert=True)

        pass

    def close_spider(self, spider):
        pass
