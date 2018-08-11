"""
    Created by Amirk on 2018-07-26.
"""
from sqlalchemy.orm import relationship

from app.model.base import Base
from sqlalchemy import Column, String, Integer, Float, Text

"""
id  # 书籍 id 号
author # 书籍作者
cat    # 分类
contentType  # 小说内容类型
cover   # 小说封面
title   # 书名
wordCount # 书籍字数
score         # 书籍评分
latelyFollower  # 追看人数
retentionRatio  # 读者存留率


updated      # 最近更新时间
lastChapter  # 最新章节
chaptersCount  # 章节数
longIntro   # 简介
"""


class BookInfo(Base):
    """书籍信息"""
    __tablename__ = "bookinfo"
    id = Column(String(100), primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(80), nullable=False)
    cat = Column(String(50))
    contentType = Column(String(50))
    cover = Column(String(200))
    wordCount = Column(Integer)
    score = Column(String(20))
    latelyFollower = Column(Integer)
    retentionRatio = Column(Float)
    updated = Column(String(50))
    lastChapter = Column(String(100))
    chaptersCount = Column(Integer)
    longIntro = Column(Text)

    # bookchapter = relationship("BookChapter", backref="bookinfo")

    def keys(self):
        return ('id', 'title', 'author','score',
                'cat','cover', 'contentType', 'wordCount',
                'latelyFollower', 'retentionRatio', 'updated',
                'lastChapter', 'chaptersCount', 'longIntro')

    @staticmethod
    def check_to_book(id=None, title=None, author=None):
        """检测数据库有没有当前书籍"""
        if id:
            book = BookInfo.query.get(id)
            if book:
                return dict(book)
        if title:
            book_all = BookInfo.query.filter_by(title=title).all()
            if title:
                return [dict(book) for book in book_all]
        if author:
            book_all = BookInfo.query.filter_by(author=author).all()
            if len(book_all) < 2:
                return False
            return [dict(book) for book in book_all]
        return False

