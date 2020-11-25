# -*- coding: utf-8 -*-
import time

import scrapy
import re
import json

from ..items import UserItem,QAItem,ArticleItem
from ..zhihu_cookie import zh_selenium
from ..mroe_package import get_cookie


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    # start_urls = ['https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=7e8848736410f393aba97135a550dcb4&desktop=true&page_number=2&limit=6&action=down&after_id=5&ad_interval=-1']

    # 入口函数
    def start_requests(self):
        api_url = zh_selenium.run()
        yield scrapy.Request(url=api_url,callback=self.first_parse,cookies=get_cookie())

    # 解析api,不断获取问答和文章数据
    def first_parse(self,response):
        # 格式化response.text
        json_data = json.loads(response.text)
        # 遍历数据
        for item in json_data['data']:
            if item['type'] == 'feed':
                # 解析问答类型的数据
                if item['target']['type'] == 'answer':
                    # 问题ID
                    question_id = item['target']['question']['id']
                    # 拼接问答页url
                    question_url = "https://www.zhihu.com/question/{0}/answers/updated".format(question_id)
                    # 解析问答页
                    yield scrapy.Request(url=question_url,callback=self.parse_question_data,meta={"question_id":question_id})
                # 解析文章类型的数据
                elif item['target']['type'] == 'article':
                    article_dict = ArticleItem()
                    # 文章ID：、
                    article_dict['article_id'] = item['target']['id']
                    # 文章作者ID
                    article_dict['article_user_id'] = item['target']['author']['id']
                    # 文章标题：
                    article_dict['article_title'] = item['target']['title']
                    # 文章内容：
                    try:
                        article_dict['article_text'] = item['target']['content']
                    except:
                        article_dict['article_text'] = item['target']['excerpt']
                    # 文章标签
                    article_dict['article_tags'] = item['target']['id']
                    # 赞同数：
                    article_dict['article_agree_count'] = item['target']['voteup_count']
                    # 评论数：
                    article_dict['article_comment_count'] = item['target']['comment_count']
                    # 文章url：
                    article_dict['article_url'] = "https://zhuanlan.zhihu.com/p/{0}".format(article_dict['article_id'])
                    # 发布时间：
                    article_dict['article_time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(item['target']['created']))
                    # 再次编辑时间
                    article_dict['article_editor_time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(item['target']['updated']))
                    # 抓取时间
                    article_dict['crawl_time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time()))
                    # 用户ID
                    user_id = item['target']['author']['id']
                    # 用户类型
                    user_type = item['target']['author']['user_type']
                    # 用户详情页
                    user_url = "https://www.zhihu.com/{0}/{1}".format(user_type,user_id)
                    # 放进管道
                    yield article_dict
                    # 解析用户页数据
                    yield scrapy.Request(url=user_url,callback=self.parse_user,meta={"url_token":item['target']['author']['url_token']})
        # 判断是否有下一页的url
        try:
            next_url = json_data['paging']['next']
        except:
            next_url = None
        # 如果有下一页，进行请求并继续解析
        if next_url != None:
            yield scrapy.Request(url=next_url, callback=self.first_parse)

    # 解析用户页
    def parse_user(self,response):
        url_token = response.request.meta['url_token']
        if url_token != '':
            search_text = re.compile('type="text/json">(.*?)</script>')
            result = re.findall(search_text, response.text)[1]
            json_data = json.loads(result)
            info = json_data['initialState']['entities']['users'][url_token]
            user_dict = UserItem()
            # 用户ID
            user_dict['user_id'] = info['id']
            # 用户类型
            user_dict['user_type'] = info['userType']
            # 用户昵称
            user_dict['nick_name'] = info['name']
            # 个性签名
            user_dict['headline'] = info['headline']
            # 粉丝数
            user_dict['followerCount'] = info['followerCount']
            # 关注数
            user_dict['followingCount'] = info['followingCount']
            # 获得赞同总数
            user_dict['voteupCount'] = info['voteupCount']
            # 获得喜欢总数
            user_dict['thankedCount'] = info['thankedCount']
            # 获得收藏总数
            user_dict['favoritedCount'] = info['favoritedCount']
            # 参与公共编辑次数
            user_dict['logsCount'] = info['logsCount']
            # 关注的话题数
            user_dict['followingTopicCount'] = info['followingTopicCount']
            # 关注的专栏数
            user_dict['followingColumnsCount'] = info['followingColumnsCount']
            # 关注的问题数
            user_dict['followingQuestionCount'] = info['followingQuestionCount']
            # 关注的收藏夹
            user_dict['followingFavlistsCount'] = info['followingFavlistsCount']
            # 回答数
            user_dict['answerCount'] = info['answerCount']
            # 文章数
            user_dict['articlesCount'] = info['articlesCount']
            # 视频数
            user_dict['zvideoCount'] = info['zvideoCount']
            # 提问数
            user_dict['questionCount'] = info['questionCount']
            # 专栏数
            user_dict['columnsCount'] = info['columnsCount']
            # 想法数
            user_dict['commercialQuestionCount'] = info['commercialQuestionCount']
            # 收藏数
            user_dict['favoriteCount'] = info['favoriteCount']
            # url_token用来进入用户详情页
            user_dict['url_token'] = info['urlToken']
            # 用户详情页
            user_dict['user_url'] = info['url']
            # 抓取时间
            user_dict['crawl_time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time()))
            yield user_dict

    # 解析问答页获取提问数据
    def parse_question_data(self, response):
        question_id = response.request.meta['question_id']
        search_text = re.compile('type="text/json">(.*?)</script>')
        result = re.findall(search_text, response.text)[1]
        json_data = json.loads(result)
        info = json_data['initialState']['entities']['questions'][str(question_id)]
        # 创建空字典
        question_dict = {}
        # 问题ID
        question_dict['question_id'] = info['id']
        # 提问者用户ID
        question_dict['question_user_id'] = info['author']['id']
        # 问题标题
        question_dict['question_title'] = info['title']
        # 问题标签
        question_dict['question_tags'] = [tag['name'] for tag in info['topics']]
        # 问题回答数
        question_dict['question_answer_count'] = info['answerCount']
        # 问题评论数
        question_dict['question_commentCount'] = info['commentCount']
        # 问题关注者人数
        question_dict['question_followerCount'] = info['followerCount']
        # 问题浏览数
        question_dict['question_visitCount'] = info['visitCount']
        # 好问题标记数
        question_dict['question_voteupCount'] = info['voteupCount']
        # 问题详情url
        question_dict['question_url'] = response.request.url
        # 提问时间
        question_dict['question_time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(info['created']))
        answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bsettings.table_of_content.enabled%3B&offset=25&limit=15&sort_by=updated".format(question_id)
        yield scrapy.Request(url=answer_url,callback=self.paesr_answer,meta=question_dict)
        # 用户ID
        user_id = info['author']['id']
        if user_id != "0":
            # 用户类型
            user_type = info['author']['userType']
            # 用户详情页
            user_url = "https://www.zhihu.com/{0}/{1}".format(user_type, user_id)
            yield scrapy.Request(url=user_url,callback=self.parse_user,meta={"url_token":info['author']['urlToken']})

    # 解析api获取回答数据
    def paesr_answer(self,response):
        json_data = json.loads(response.text)
        for info in json_data['data']:
            QA_dict = QAItem()
            # 回答ID
            QA_dict['answer_id'] = info['id']
            # 回答者用户ID
            QA_dict['answer_user_id'] = info['author']['id']
            # 回答内容
            try:
                QA_dict['answer_text'] = info['content']
            except:
                QA_dict['answer_text'] = info['excerpt']
            # 回答赞同数
            QA_dict['answer_voteup_count'] = info['voteup_count']
            # 回答评论数
            QA_dict['answer_comment_count'] = int(info['comment_count'])
            # 回答时间
            QA_dict['answer_time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(info['created_time']))
            # 问题ID
            QA_dict['question_id'] = response.request.meta['question_id']
            # 提问者用户ID
            QA_dict['question_user_id'] = response.request.meta['question_user_id']
            # 问题标题
            QA_dict['question_title'] = response.request.meta['question_title']
            # 问题标签
            QA_dict['question_tags'] = response.request.meta['question_tags']
            # 问题回答数
            QA_dict['question_answer_count'] = response.request.meta['question_answer_count']
            # 问题评论数
            QA_dict['question_commentCount'] = response.request.meta['question_commentCount']
            # 问题关注者人数
            QA_dict['question_followerCount'] = response.request.meta['question_followerCount']
            # 问题浏览数
            QA_dict['question_visitCount'] = response.request.meta['question_visitCount']
            # 好问题标记数
            QA_dict['question_voteupCount'] = response.request.meta['question_voteupCount']
            # 问题详情url
            QA_dict['question_url'] = response.request.meta['question_url']
            # 提问时间
            QA_dict['question_time'] = response.request.meta['question_time']
            # 抓取时间
            QA_dict['crawl_time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time()))
            yield QA_dict
            # 用户ID
            user_id = info['author']['id']
            if user_id != "0":
                # 用户类型
                user_type = info['author']['user_type']
                # 用户详情页
                user_url = "https://www.zhihu.com/{0}/{1}".format(user_type, user_id)
                yield scrapy.Request(url=user_url, callback=self.parse_user,meta={"url_token":info['author']['url_token']})
        try:
            next_url = json_data['paging']['next']
        except:
            next_url = None
        if next_url != None:
            yield scrapy.Request(url=next_url, callback=self.paesr_answer,meta=response.request.meta)