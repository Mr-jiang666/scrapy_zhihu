# coding:utf-8
from sqlalchemy import create_engine, Integer,String,Text,DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

# 创建数据库的连接
engine = create_engine("mysql://root:abc123456@127.0.0.1:3306/db_zhihu?charset=utf8mb4")
# 操作数据库，需要我们创建一个session
Session = sessionmaker(bind=engine)
# 声明一个基类
Base = declarative_base()


# 问答数据表
class zh_question_answer(Base):
    # 表名称
    __tablename__ = 'zh_question_answer'
    # 回答ID
    answer_id = Column(Integer, primary_key=True)
    # 回答者用户ID
    answer_user_id = Column(String(length=32))
    # 回答内容
    answer_text = Column(LONGTEXT)
    # 赞同数
    answer_voteup_count = Column(Integer)
    # 评论数
    answer_comment_count = Column(Integer,default=0)
    # 问题ID
    question_id = Column(Integer)
    # 提问者用户ID
    question_user_id = Column(String(length=32))
    # 问题标题
    question_title = Column(String(length=100))
    # 问题标签
    question_tags = Column(String(length=100))
    # 问题回答数
    question_answer_count = Column(Integer)
    # 问题评论数
    question_commentCount = Column(Integer)
    # 问题关注者人数
    question_followerCount = Column(Integer)
    # 问题浏览数
    question_visitCount = Column(Integer)
    # 好问题标记数
    question_voteupCount = Column(Integer)
    # 问题详情url
    question_url = Column(String(length=200))
    # 问题发起时间
    question_time = Column(DateTime)
    # 回答时间
    answer_time = Column(DateTime)
    # 抓取日期
    crawl_time = Column(DateTime)


# 文章数据表
class zh_article(Base):
    # 表名称
    __tablename__ = 'zh_article'
    # 文章ID
    article_id = Column(Integer, primary_key=True)
    # 文章作者ID
    article_user_id = Column(String(length=32))
    # 文章标题
    article_title = Column(String(length=100))
    # 文章内容
    article_text = Column(LONGTEXT)
    # 文章标签
    article_tags = Column(String(length=100))
    # 赞同数
    article_agree_count = Column(Integer)
    # 评论数
    article_comment_count = Column(Integer)
    # 文章url
    article_url = Column(String(length=200))
    # 发布时间
    article_time = Column(DateTime)
    # 再次编辑时间
    article_editor_time = Column(DateTime)
    # 抓取日期
    crawl_time = Column(DateTime)


# 用户数据表
class zh_user(Base):
    # 表名称
    __tablename__ = 'zh_user'
    # 用户ID
    user_id = Column(String(length=32), primary_key=True)
    # 用户类型
    user_type = Column(String(length=20))
    # 用户昵称
    nick_name = Column(String(length=50))
    # 粉丝数
    followerCount = Column(Integer,default=0)
    # 个性签名
    headline = Column(String(length=100))
    # 关注数
    followingCount = Column(Integer,default=0)
    # 获得赞同总数
    voteupCount = Column(Integer,default=0)
    # 获得喜欢总数
    thankedCount = Column(Integer,default=0)
    # 获得收藏总数
    favoritedCount = Column(Integer,default=0)
    # 参与公共编辑次数
    logsCount = Column(Integer,default=0)
    # 关注的话题数
    followingTopicCount = Column(Integer,default=0)
    # 关注的专栏数
    followingColumnsCount = Column(Integer,default=0)
    # 关注的问题数
    followingQuestionCount = Column(Integer,default=0)
    # 关注的收藏夹
    followingFavlistsCount = Column(Integer,default=0)
    # 回答数
    answerCount = Column(Integer,default=0)
    # 文章数
    articlesCount = Column(Integer,default=0)
    # 视频数
    zvideoCount = Column(Integer,default=0)
    # 提问数
    questionCount = Column(Integer,default=0)
    # 专栏数
    columnsCount = Column(Integer,default=0)
    # 想法数
    commercialQuestionCount = Column(Integer,default=0)
    # 收藏数
    favoriteCount = Column(Integer,default=0)
    # url_token用来进入用户详情页
    url_token = Column(String(length=100))
    # 用户详情页url
    user_url = Column(String(length=200))
    # 抓取日期
    crawl_time = Column(DateTime)


# 入库逻辑，数据清洗
class zh_data(object):
    # 重写父类
    def __init__(self):
        # 实例化session信息
        self.mysql_session = Session()

    # 商品信息数据的存储方法
    def zh_QA_data(self, item):
        # 存储的数据结构
        data = zh_question_answer(
            # 回答ID
            answer_id = int(item['answer_id']),
            # 回答者用户ID
            answer_user_id = item['answer_user_id'],
            # 回答内容
            answer_text = item['answer_text'],
            # 赞同数
            answer_voteup_count = int(item['answer_voteup_count']),
            # 评论数
            answer_comment_count = int(item['answer_comment_count']),
            # 问题ID
            question_id = int(item['question_id']),
            # 提问者用户ID
            question_user_id = item['question_user_id'],
            # 问题标题
            question_title = item['question_title'],
            # 问题标签
            question_tags = str(item['question_tags']),
            # 问题回答数
            question_answer_count = int(item['question_answer_count']),
            # 问题评论数
            question_commentCount = int(item['question_commentCount']),
            # 问题关注数
            question_followerCount = int(item['question_followerCount']),
            # 问题浏览数
            question_visitCount = int(item['question_visitCount']),
            # 好问题标记数
            question_voteupCount = int(item['question_voteupCount']),
            # 问题详情url
            question_url = item['question_url'],
            # 问题发起时间
            question_time = item['question_time'],
            # 回答时间
            answer_time = item['answer_time'],
            # 抓取日期
            crawl_time = item['crawl_time']
        )
        # 数据去重
        query_result = self.mysql_session.query(zh_question_answer).filter(zh_question_answer.answer_id == item['answer_id']).first()
        if query_result:
            try:
                # 更新数据
                self.mysql_session.query(zh_question_answer).filter(zh_question_answer.answer_id == item['answer_id']).update(item)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('zh_question_answer数据表update：%s：%s' % (item['answer_id'], item['question_id']))
            except Exception as e:
                with open("./zh_log.txt", "a+", encoding="utf-8") as f:
                    f.write("zh_question_answer update ERROR：%s:\n%s" % (item, e))
                f.close()
        else:
            try:
                # 插入数据
                self.mysql_session.add(data)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('zh_question_answer数据表add：%s：%s' % (item['answer_id'], item['question_id']))
            except Exception as e:
                with open("./zh_log.txt", "a+", encoding="utf-8") as f:
                    f.write("zh_question_answer add ERROR：%s:\n%s" % (item, e))
                f.close()

    # 获取类别信息
    def zh_article_data(self, item):
        # 存储的数据结构
        data = zh_article(
            # 文章ID
            article_id = item['article_id'],
            # 文章作者ID
            article_user_id = item['article_user_id'],
            # 文章标题
            article_title = item['article_title'],
            # 文章内容
            article_text = item['article_text'],
            # 文章标签
            article_tags = item['article_tags'],
            # 赞同数
            article_agree_count = item['article_agree_count'],
            # 评论数
            article_comment_count = item['article_comment_count'],
            # 文章url
            article_url = item['article_url'],
            # 发布时间
            article_time = item['article_time'],
            # 再次编辑时间
            article_editor_time = item['article_editor_time'],
            # 抓取日期
            crawl_time = item['crawl_time']
        )
        # 数据去重
        query_result = self.mysql_session.query(zh_article).filter(zh_article.article_id == item['article_id']).first()
        if query_result:
            try:
                # 更新数据
                self.mysql_session.query(zh_article).filter(zh_article.article_id == item['article_id']).update(item)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('zh_article数据表update：%s：%s' % (item['article_id'], item['article_title']))
            except Exception as e:
                with open("./zh_log.txt", "a+", encoding="utf-8") as f:
                    f.write("zh_article update ERROR：%s:\n%s" % (item, e))
                f.close()
        else:
            try:
                # 插入数据
                self.mysql_session.add(data)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('zh_article数据表add：%s：%s' % (item['article_id'], item['article_title']))
            except Exception as e:
                with open("./zh_log.txt", "a+", encoding="utf-8") as f:
                    f.write("zh_article add ERROR：%s:\n%s" % (item, e))
                f.close()

    # 获取类别信息
    def zh_user_data(self, item):
        # 存储的数据结构
        data = zh_user(
            # 用户ID
            user_id = item['user_id'],
            # 用户类型
            user_type = item['user_type'],
            # 用户昵称
            nick_name = item['nick_name'],
            # 粉丝数
            followingCount = int(item['followingCount']),
            # 获得赞同总数
            voteupCount = int(item['voteupCount']),
            # 获得喜欢总数
            thankedCount = int(item['thankedCount']),
            # 获得收藏总数
            favoritedCount = int(item['favoritedCount']),
            # 参与公共编辑次数
            logsCount = int(item['logsCount']),
            # 关注的话题数
            followingTopicCount = int(item['followingTopicCount']),
            # 关注的专栏数
            followingColumnsCount = int(item['followingColumnsCount']),
            # 关注的问题数
            followingQuestionCount = int(item['followingQuestionCount']),
            # 关注的收藏夹
            followingFavlistsCount = int(item['followingFavlistsCount']),
            # 回答数
            answerCount = int(item['answerCount']),
            # 文章数
            articlesCount = int(item['articlesCount']),
            # 视频数
            zvideoCount = int(item['zvideoCount']),
            # 提问数
            questionCount = int(item['questionCount']),
            # 专栏数
            columnsCount = int(item['columnsCount']),
            # 想法数
            commercialQuestionCount = int(item['commercialQuestionCount']),
            # 收藏数
            favoriteCount = int(item['favoriteCount']),
            # 个性签名
            headline = item['headline'],
            # url_token用来进入用户详情页
            url_token = item['url_token'],
            # 用户详情页url
            user_url = item['user_url'],
            # 抓取日期
            crawl_time = item['crawl_time']
        )
        # 数据去重
        query_result = self.mysql_session.query(zh_user).filter(zh_user.user_id == item['user_id']).first()
        if query_result:
            try:
                # 更新数据
                self.mysql_session.query(zh_user).filter(zh_user.user_id == item['user_id']).update(item)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('zh_user数据表update：%s：%s' % (item['user_id'], item['nick_name']))
            except Exception as e:
                with open("./zh_log.txt", "a+", encoding="utf-8") as f:
                    f.write("zh_user update ERROR：%s:\n%s" % (item, e))
                f.close()
        else:
            try:
                # 插入数据
                self.mysql_session.add(data)
                # 提交数据到数据库
                self.mysql_session.commit()
                print('zh_user数据表add：%s：%s' % (item['user_id'], item['nick_name']))
            except Exception as e:
                with open("./zh_log.txt", "a+", encoding="utf-8") as f:
                    f.write("zh_user add ERROR：%s:\n%s" % (item, e))
                f.close()


# 实例化类对象
zh_mysql = zh_data()


if __name__ == '__main__':
    # 创建数据表
    zh_article.metadata.create_all(engine)

