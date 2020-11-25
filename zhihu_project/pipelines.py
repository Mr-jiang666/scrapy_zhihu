# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from zhihu_project.models.MySQLModel import zh_mysql
from .items import UserItem,QAItem,ArticleItem

class ZhihuProjectPipeline:
    def process_item(self, item, spider):
        if isinstance(item,UserItem):
            # print(item)
            zh_mysql.zh_user_data(item)
        elif isinstance(item,QAItem):
            # print(item)
            zh_mysql.zh_QA_data(item)
        elif isinstance(item,ArticleItem):
            # print(item)
            zh_mysql.zh_article_data(item)
        return item
