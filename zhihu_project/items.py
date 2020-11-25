# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QAItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 回答ID
    answer_id = scrapy.Field()
    # 回答者用户ID
    answer_user_id = scrapy.Field()
    # 回答内容
    answer_text = scrapy.Field()
    # 回答赞同数
    answer_voteup_count = scrapy.Field()
    # 回答评论数
    answer_comment_count = scrapy.Field()
    # 回答时间
    answer_time = scrapy.Field()
    # 问题ID
    question_id = scrapy.Field()
    # 提问者用户ID
    question_user_id = scrapy.Field()
    # 问题标题
    question_title = scrapy.Field()
    # 问题标签
    question_tags = scrapy.Field()
    # 问题回答数
    question_answer_count = scrapy.Field()
    # 问题评论数
    question_commentCount = scrapy.Field()
    # 问题关注者人数
    question_followerCount = scrapy.Field()
    # 问题浏览数
    question_visitCount = scrapy.Field()
    # 好问题标记数
    question_voteupCount = scrapy.Field()
    # 问题详情url
    question_url = scrapy.Field()
    # 提问时间
    question_time = scrapy.Field()
    # 抓取时间
    crawl_time = scrapy.Field()


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 用户ID
    user_id = scrapy.Field()
    # 用户类型
    user_type = scrapy.Field()
    # 用户昵称
    nick_name = scrapy.Field()
    # 个性签名
    headline = scrapy.Field()
    # 粉丝数
    followerCount = scrapy.Field()
    # 关注数
    followingCount = scrapy.Field()
    # 获得赞同总数
    voteupCount = scrapy.Field()
    # 获得喜欢总数
    thankedCount = scrapy.Field()
    # 获得收藏总数
    favoritedCount = scrapy.Field()
    # 参与公共编辑次数
    logsCount = scrapy.Field()
    # 关注的话题数
    followingTopicCount = scrapy.Field()
    # 关注的专栏数
    followingColumnsCount = scrapy.Field()
    # 关注的问题数
    followingQuestionCount = scrapy.Field()
    # 关注的收藏夹
    followingFavlistsCount = scrapy.Field()
    # 回答数
    answerCount = scrapy.Field()
    # 文章数
    articlesCount = scrapy.Field()
    # 视频数
    zvideoCount = scrapy.Field()
    # 提问数
    questionCount = scrapy.Field()
    # 专栏数
    columnsCount = scrapy.Field()
    # 想法数
    commercialQuestionCount = scrapy.Field()
    # 收藏数
    favoriteCount = scrapy.Field()
    # url_token用来进入用户详情页
    url_token = scrapy.Field()
    # 用户详情页
    user_url = scrapy.Field()
    # 抓取时间
    crawl_time = scrapy.Field()


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文章ID
    article_id = scrapy.Field()
    # 文章作者ID
    article_user_id = scrapy.Field()
    # 文章标题
    article_title = scrapy.Field()
    # 文章内容
    article_text = scrapy.Field()
    # 文章标签
    article_tags = scrapy.Field()
    # 赞同数
    article_agree_count = scrapy.Field()
    # 评论数
    article_comment_count = scrapy.Field()
    # 文章url
    article_url = scrapy.Field()
    # 发布时间
    article_time = scrapy.Field()
    # 再次编辑时间
    article_editor_time = scrapy.Field()
    # 抓取日期
    crawl_time = scrapy.Field()
